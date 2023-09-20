from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem
from statics import interpret_days
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QMainWindow


class CalendarWidget(QTableWidget):
    """
    Calendar widget that can display the course schedule information in calendar view
    """
    def __init__(self, parent: QMainWindow = None):
        super().__init__(10, 5)

        self.setParent(parent)
        self.draw_empty_table()
        self.courses = []

    def draw_empty_table(self) -> None:
        """
        Puts days and times of the week as the headers of the table
        :return: None
        """
        self.setHorizontalHeaderLabels(["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"])
        self.setVerticalHeaderLabels(
            ["8:00", "9:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00", "17:00"])
        self.setEditTriggers(QTableWidget.NoEditTriggers)

    def populate_calendar(self) -> None:
        """
        Fills the calendar spots with the course information
        :return: None
        """

        # Iterate through course list
        for course in self.courses:
            # Gets schedule, finds which day/days in the week lecture is delivered and gets color of class widget
            schedule = course.class_details['Schedule']
            days = interpret_days(schedule[0])
            background_color = course.color

            # Handles chance for a course to be had multiple days
            if None in days:
                self.create_cells(schedule[1], days[0], schedule[2] - schedule[1], background_color, course.class_name)
            else:
                for day in days:
                    self.create_cells(schedule[1], day, schedule[2] - schedule[1], background_color, course.class_name)

    def create_cells(self, row: int, column: int, row_span: int, color: QColor, course_name: str) -> None:
        """
        Creates cell in table view that has the course name, color and time span
        :param row: starting hour
        :param column: day
        :param row_span: lecture duration
        :param color: color of class widget
        :param course_name: name of the course
        :return: None
        """
        # Create a QTableWidgetItem
        item = QTableWidgetItem(course_name)
        item.setBackground(QColor(color[0], color[1], color[2]))

        # Set the item as the cell's item
        self.setItem(row, column, item)

        # Set the cell's span
        self.setSpan(row, column, row_span, 1)
