from base_question_processor import BaseQuestionProcessor

class CommandQuestionProcessor(BaseQuestionProcessor):
    def __init__(self, question):
        super(CommandQuestionProcessor, self).__init__()

    def process(self):
        return super(CommandQuestionProcessor, self).process()