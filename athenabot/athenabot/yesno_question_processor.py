import nltk

from base_question_processor import BaseQuestionProcessor

class YesnoQuestionProcessor(BaseQuestionProcessor):
    def __init__(self, question):
        super(YesnoQuestionProcessor, self).__init__(question)

    def process(self):
        keywords = self.get_keywords()
        return super(YesnoQuestionProcessor, self).process(keywords, True)

    def get_keywords(self):
        '''
        Keywords will be words having POS tags as noun:
        NN, NNP, NNPS, NNS
        '''
        keywords = set()
        req_pos_tags = set(['NN', 'NNP', 'NNPS', 'NNS'])
        question_words = nltk.word_tokenize(self.question.lower().strip())
        pos_tags = nltk.pos_tag(question_words)
        for word, tag in pos_tags:
            if tag in req_pos_tags and not word == 'athenahealth':
                keywords.add(word)
        return keywords