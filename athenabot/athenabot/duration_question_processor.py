from base_question_processor import BaseQuestionProcessor
from constants import DURATION_KEYWORDS

class DurationQuestionProcessor(BaseQuestionProcessor):
    def __init__(self, question):
        super(DurationQuestionProcessor, self).__init__(question)

    def process(self):
        return super(DurationQuestionProcessor, self).process(DURATION_KEYWORDS, True, True)