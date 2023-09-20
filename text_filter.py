import yake
from heapq import nlargest
from gui.class_widget import ClassBox


class TextFilter:

    def __init__(self):
        self.kw_extractor = yake.KeywordExtractor()
        self.keywords = []

        self.scores = []
        
    def extract_keywords(self, doc):
        self.keywords = self.kw_extractor.extract_keywords(doc)
    
    def rank_classes(self, course: ClassBox):

        details = course.class_details
        score = 0
        description = details['Description']
        units = details['Units']
        full_text = description + " " + units

        for word in self.keywords:
            keyWord = word[0]
            
            if keyWord in full_text:
                score += 1

        if score > 0:
            course.set_percentage(score)

            return True
        else:
            return False
