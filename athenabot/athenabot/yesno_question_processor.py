from base_question_processor import BaseQuestionProcessor

class YesnoQuestionProcessor(BaseQuestionProcessor):
    def __init__(self, question):
        super(YesnoQuestionProcessor, self).__init__(question)

    def process(self):
        return super(YesnoQuestionProcessor, self).process()