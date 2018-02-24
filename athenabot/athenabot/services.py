#from sentence_similarity import similarity
import nltk
import os
from nltk.corpus import stopwords
import re, math
from collections import Counter
from question_parser import QuestionParser
from constants import QuestionType

from yesno_question_processor import YesnoQuestionProcessor
from duration_question_processor import DurationQuestionProcessor
from command_question_processor import CommandQuestionProcessor
from distance_question_processor import DistanceQuestionProcessor
from count_question_processor import CountQuestionProcessor
from who_question_processor import WhoQuestionProcessor
from generic_question_processor import GenericQuestionProcessor

class Chatbot(object):
    def __init__(self, question):
        self.question = question
        self.question_type_processor_hash = {   QuestionType.QUESTION_YES_NO     :   YesnoQuestionProcessor,
                                                QuestionType.QUESTION_COMMAND    :   CommandQuestionProcessor,
                                                QuestionType.QUESTION_DURATION   :   DurationQuestionProcessor,
                                                QuestionType.QUESTION_DISTANCE   :   DistanceQuestionProcessor,
                                                QuestionType.QUESTION_COUNT      :   CountQuestionProcessor,
                                                QuestionType.QUESTION_WHO        :   WhoQuestionProcessor,
                                                QuestionType.QUESTION_GENERIC    :   GenericQuestionProcessor
                                            }

    def process(self):
        ques_type = self.get_question_type()
        question_processor = self.question_type_processor_hash.get(ques_type)
        if question_processor:
            obj = question_processor(self.question)
            print obj.process()
        else:
            obj = WhoQuestionProcessor(self.question)
            print obj.process()


    def get_question_type(self):
        ques_parser = QuestionParser(self.question)
        question_type = ques_parser.get_question_type()
        print 'question type: %s' % question_type
        return question_type


if __name__ == '__main__':
    question1 = 'Is athenahealth best in KLAS?'
    question2 = 'How long are wellness visits scheduled between doctors and patients?'
    question3 = 'How many min in a day can be saved by using epocrates?'
    question4 = 'What is the number of providers on athenahealth network?'
    question5 = 'Take me to driving quality page in hppn (High-performing performance network).'

    question6 = 'How much is decrease in post-visit documentation rate ?'
    question7 = 'What percentage of clients avoided PQRS penalties using athenahealth ?'
    question8 = 'Who is the director of the Empathy and Relational Science Program at Massachusetts General Hospital ?'
    question9 = 'Name an internist in San Francisco'
    question10 = 'How much have the appointments time shrunk by using athenahealth ?'
    question11 = 'What does Berenson says about payment reform ?'

    questions = [question11, question10, question9, question8, question1, question2, question3, question4, question5, question6, question7]
    for question in questions:
        print question
        obj = Chatbot(question)
        obj.process()



