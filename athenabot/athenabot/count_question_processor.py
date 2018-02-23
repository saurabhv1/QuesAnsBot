from base_question_processor import BaseQuestionProcessor

class CountQuestionProcessor(BaseQuestionProcessor):
    def __init__(self, question):
        super(CountQuestionProcessor, self).__init__(question)

    def process(self):
        #return super(CountQuestionProcessor, self).process()
        return super(CountQuestionProcessor, self).process([], True, True)