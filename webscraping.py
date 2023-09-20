from bs4 import BeautifulSoup
from selenium import webdriver
from time import sleep
from selenium.webdriver.common.by import By
from typing import Tuple
from statics import save_dict_to_json
from tqdm import tqdm


class CourseScrapper:

    def __init__(self):
        self.URL = 'https://catalog.registrar.ucla.edu/search?q=EC+ENGR&ct=all'
        self.driver = webdriver.Chrome()
        self.course_dict = dict()
        self.driver.get(self.URL)
        # Sleep to allow the webpage to load
        sleep(4)
        self.max_page_number = self._get_max_page_number()

    def _get_max_page_number(self) -> int:
        """
        Finds the maximum number of pages to iterate through every course page by reading the second page button
        :return: maximum number of pages
        """
        first_button = self.driver.find_element(By.ID, f'pagination-page-{2}')
        return int(first_button.get_attribute("aria-label")[-2:])

    def _find_class_and_link(self) -> None:
        """
        Finds the class name, adds it as an item in course_dict that contains a dict of the link of the class details
        :return: None
        """
        # Parse the HTML content with BeautifulSoup
        soup = BeautifulSoup(self.driver.page_source, 'html.parser')

        # Find the div element containing the list of classes
        class_div = soup.find('div', {'id': 'search-results'})

        a_tags = class_div.find_all('a')
        for a_tag in a_tags:
            div = a_tag.find('span', {'class': 'result-item-title'})
            course_name = div.text.strip()
            href = a_tag['href']

            # if to only take electrical engineering courses
            if "EC ENGR" in course_name:
                self.course_dict[course_name] = {'href': "https://catalog.registrar.ucla.edu" + href}

    def get_all_courses(self) -> None:
        """
        Iterates through every page and adds the courses and their links to course_dict
        :return: None
        """
        for page in tqdm(range(1, self.max_page_number+1)):
            next_button = self.driver.find_element(By.ID, f'pagination-page-{page}')
            self.driver.execute_script("arguments[0].click();", next_button)
            sleep(6)
            self._find_class_and_link()
        print(len(self.course_dict))
        print(self.course_dict)

    def _extract_course_data(self) -> Tuple[str, str, str, str, str]:
        """
        Extracts course details from course page
        :return:
        """
        soup = BeautifulSoup(self.driver.page_source, 'html.parser')
        class_units_element = soup.select('h5[class^="introDetails__sub_heading"]')
        class_units = class_units_element[1].text.strip()
        class_description_element = soup.find('div', {'id': 'Description'})
        class_description_text = class_description_element.find('div', {'class': 'readmore-content-wrapper'}).\
            find('p').text.strip()
        class_details = soup.find('div', {'data-testid': 'attributes-table'})
        a_elements = class_details.find_all('a', {'id': 'College/School'})
        college, department, subject_area = [a.get('aria-label') for a in a_elements]

        return class_description_text, college, department, subject_area, class_units

    def _open_course_info(self, course: str) -> None:
        """
        Opens the course page
        :param course: name of course as written in dictionary key
        :return: None
        """
        course_url = self.course_dict[course]['href']
        print(course_url)
        self.driver.get(course_url)
        sleep(4)

    def get_course_info(self) -> None:
        """
        Iterates through every course and adds the extra details
        :return: None
        """
        for course in tqdm(list(self.course_dict.keys())):
            self._open_course_info(course)
            description, college, department, subject_area, units = self._extract_course_data()
            self.course_dict[course]['Description'] = description
            self.course_dict[course]['College'] = college
            self.course_dict[course]['Department'] = department
            self.course_dict[course]['Subject area'] = subject_area
            self.course_dict[course]['Units'] = units

    def create_course_data(self) -> None:
        """
        Finds all courses, all course details and saves it in a json file
        :return: None
        """
        self.get_all_courses()
        self.get_course_info()
        self._quit_driver()
        save_dict_to_json(self.course_dict, 'course_data.json')

    def _quit_driver(self) -> None:
        """
        Quits the selenium driver
        :return: None
        """
        self.driver.quit()


if __name__ == "__main__":
    course_scrapper = CourseScrapper()
    course_scrapper.create_course_data()
