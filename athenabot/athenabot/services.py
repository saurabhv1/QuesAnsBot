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

class Chatbot(object):
    def __init__(self, question):
        #self.stop_words = set(stopwords.words('english'))
        #self.word_pattern = re.compile(r'\w+')
        self.question = question
        self.question_type_processor_hash = {   QuestionType.QUESTION_YES_NO     :   YesnoQuestionProcessor,
                                                QuestionType.QUESTION_COMMAND    :   CommandQuestionProcessor,
                                                QuestionType.QUESTION_DURATION   :   DurationQuestionProcessor,
                                                QuestionType.QUESTION_DISTANCE   :   DistanceQuestionProcessor,
                                                QuestionType.QUESTION_COUNT      :   CountQuestionProcessor
                                            }
        #self.tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')

    def process(self):
        ques_type = self.get_question_type()
        question_processor = self.question_type_processor_hash.get(ques_type)
        #import pdb; pdb.set_trace()
        if question_processor:
            obj = question_processor(self.question)
            print obj.process()


    def get_question_type(self):
        ques_parser = QuestionParser(self.question)
        question_type = ques_parser.get_question_type()
        print 'question type: %s' % question_type
        return question_type

    def answer(self, question):
        #import pdb; pdb.set_trace()
        return self.get_best_sentence_match(question)

    def get_best_sentence_match(self, question_words):
        max_score = -1
        result = ''
        all_files = self.get_all_files()
        for count, file in enumerate(all_files):
            file = '../train/data/' + file
            with open(file) as f:
                try:
                    next(f)
                except:
                    break
                for line in f:
                    if len(line) < 8:
                        continue
                    clean_line = line
                    #clean_line = self.remove_stopwords(line)
                    try:
                        #sentences = (self.tokenizer.tokenize(clean_line))
                        sentences = clean_line.split('.')
                    except:
                        continue
                    for sentence in sentences:
                        if True: #try:
                            if len(sentence) < 8:
                                continue
                            clean_sentence = self.remove_stopwords(sentence)
                            #sim_score = similarity(question, sentence, False)
                            #sim_score = self.get_similarity(question_words, clean_sentence)
                            #print sim_score, sentence
                            vector1 = self.text_to_vector(clean_sentence)
                            vector2 = self.text_to_vector(question_words)
                            cosine = self.get_cosine(vector2, vector1)
                            if cosine > max_score:
                                max_score = cosine
                                result = sentence
                        #except:
                        #    continue
        return result, max_score


    def remove_stopwords(self, line):
        return ' '.join([i for i in line.lower().split() if i not in self.stop_words])


    def get_all_files(self):
        data_dir = '../train/data'
        all_files = [f for f in os.listdir(data_dir) if not(f == 'urls.txt')]
        return all_files

    def get_similarity(self, question_words, sentence):
        sent_words = set(sentence.lower().split())
        same_words = sent_words.intersection(question_words)
        return len(same_words)


    def get_cosine(self, vec1, vec2):
        intersection = set(vec1.keys()) & set(vec2.keys())
        numerator = sum([vec1[x] * vec2[x] for x in intersection])
        import pdb; pdb.set_trace()
        sum1 = sum([vec1[x]**2 for x in vec1.keys()])
        sum2 = sum([vec2[x]**2 for x in vec2.keys()])
        denominator = math.sqrt(sum1) * math.sqrt(sum2)

        if not denominator:
            return 0.0
        else:
            return float(numerator) / denominator

    def text_to_vector(self, text):
        words = self.word_pattern.findall(text)
        #import pdb; pdb.set_trace()
        return Counter(words)












if __name__ == '__main__':
    #question = 'Is athenahealth best in KLAS?'
    #question = 'How long are wellness visits scheduled between doctors and patients?'
    question = 'How many min in a day can be saved by using epocrates?'
    #question = 'What is the number of providers on athenahealth network?'
    obj = Chatbot(question)
    obj.process()
    #clean_question = obj.remove_stopwords(question)
    #import pdb; pdb.set_trace()
    #ques_words = set(clean_question.split())
    #print obj.answer(clean_question)



