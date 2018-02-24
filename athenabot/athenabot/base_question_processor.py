import re, math
import os
from collections import Counter
from nltk.corpus import stopwords
import nltk.data
from string import ascii_letters
from constants import DURATION_KEYWORDS, DISTANCE_KEYWORDS, COUNT_KEYWORDS, ALL_KEYWORDS
from utils import is_number

class BaseQuestionProcessor(object):
    def __init__(self, question):
        self.stop_words = set(stopwords.words('english'))
        self.question = self.clean_question(question)
        self.word_pattern = re.compile(r'\w+')
        self.tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
        self.data_dir = '../train/data_kw/'

    def clean_question(self, question):
        question = self.remove_stopwords(question)
        question = question.replace('athena', '').replace('athenahealth','')
        return question

    def process(self, keywords = [], clean_sentence=False, number_present=False, pos_tag=None):
        data_dir = '../train/data_kw/'
        best_sentence, score = self.get_best_sentence_match(keywords, clean_sentence, number_present, pos_tag)
        words = best_sentence.split()
        nearby_words = []
        if len(words) > 20:
            generic_keywords = self.get_generic_keywords()
            for pos, word in enumerate(words):
                if word in generic_keywords:
                    nearby_words = self.get_previous_next_words(words, pos, len(words))
                    break
        return ' '.join(nearby_words) if len(nearby_words) > 0 else best_sentence


    def get_best_sentence_match(self, keywords, clean_sentence, number_present, req_pos_tag):
        max_score = -1
        result = ''
        all_files = self.get_all_files()
        for file in all_files:
            file = self.data_dir + file
            file_content = open(file).read()
            sentences = self.get_sentences(file_content, file)
            for sentence in sentences:
                cleaned_sentence, words = self.clean_sentence(sentence, file)
                if len(keywords) > 0 and not any(keyword in words for keyword in keywords):
                    continue
                #if file.endswith('athenaclinicalsehr.txt') and '23' in cleaned_sentence:
                #    import pdb; pdb.set_trace()
                if number_present and not any(is_number(word) for word in words):
                    continue
                if req_pos_tag:
                    pos_tags = nltk.pos_tag(words)
                    if not any(pos_tag[1] == req_pos_tag for pos_tag in pos_tags):
                        continue
                vector1 = self.text_to_vector(cleaned_sentence)
                vector2 = self.text_to_vector(self.question)
                cosine = self.get_cosine_score(vector2, vector1)
                if cosine > max_score:
                    max_score = cosine
                    result = sentence
        return result, max_score

    def clean_sentence(self, sentence, file):
        final_words = []
        #if file.endswith('athenaclinicalsehr.txt'):# and 'documentation  rate' in sentence:
        #    import pdb; pdb.set_trace()
        sentence = self.remove_stopwords(sentence)
        words = sentence.split()
        new_words = ['']
        for word in words:     
            match = re.match(r"([0-9]+)([a-z]+)", word, re.I) # For cases like 20time
            if match:
                new_words =  match.groups()
            else:
                match = re.match(r"([0-9]+),([0-9]+)", word, re.I) # for cases like 200,00
                if match:
                    new_words = [''.join(match.groups())]
                else:
                    new_words = [word]
            final_words += new_words
        return ' '.join(final_words), final_words


    def get_sentences(self, content, file):
        res = []
        #if file.endswith('athenaclinicalsehr.txt'):# and 'documentation  rate' in sentence:
        #    import pdb; pdb.set_trace()
        temp = content.replace('. ', '||').replace('*', '||').replace(':', '||').replace('.\n', ' ').replace(' ', '||')
        words = temp.split('||')
        cur_words = []
        for word in words:
            #if word == 'Helen':
            #    import pdb; pdb.set_trace()
            if self.is_sentence_breaker(word):
                res.append(' '.join(cur_words))
                cur_words = []
            else:
                cur_words.append(word)
        return res


    def is_sentence_breaker(self, word):
        breaker_words = ['watch', 'demo']
        #if word == '23%':
        #    import pdb; pdb.set_trace()
        if re.match(r"([0-9]+),([0-9]+)", word, re.I): # for cases like 200,000
            return False
        elif re.match(r"([0-9]+)%", word, re.I): # for cases like 20%
            return False
        elif re.match(r"([a-z]+)-([a-z]+)", word, re.I): # cses like west-wind
            return False
        if not word.isalnum() or word in breaker_words:
            return True
        return False

    def get_previous_words(self, words, cur_pos, count=10):
        previous_pos = max(0, cur_pos-count)
        return ' '.join(words[previous_pos: cur_pos+1])

    def get_next_words(self, words, cur_pos, total_words, count=10):
        next_pos = min(total_words-1, cur_pos+count)
        return ' '.join(words[cur_pos-1: next_pos+1])

    def get_generic_keywords(self):
        '''
        Get all the forms of Noun occuring in the question
        viz: NN, NNP, NNPS, NNS
        '''
        keywords = set()
        question_words = nltk.word_tokenize(self.question)
        pos_tags = nltk.pos_tag(question_words)
        for word, tag in pos_tags:
            if tag.startswith('NN'):
                keywords.add(word)
        print keywords
        return keywords

    def get_previous_next_words(self, content, cur_pos, total_words, count=10):
        previous_pos = max(0, cur_pos-count)
        next_pos = min(total_words-1, cur_pos+count)
        return content[previous_pos: next_pos]

    def clean_result(self, result):
        if '.' in result:
            pass


    def text_to_vector(self, text):
        words = self.word_pattern.findall(text)
        return Counter(words)

    def get_cosine_score(self, vec1, vec2):
        intersection = set(vec1.keys()) & set(vec2.keys())
        numerator = sum([vec1[x] * vec2[x] for x in intersection])
        sum1 = sum([vec1[x]**2 for x in vec1.keys()])
        sum2 = sum([vec2[x]**2 for x in vec2.keys()])
        denominator = math.sqrt(sum1) * math.sqrt(sum2)
        return float(numerator) / denominator if denominator else 0.0

    def get_all_files(self):
        data_dir = '../train/data_kw'
        all_files = [f for f in os.listdir(data_dir) if not(f == 'urls.txt')]
        return all_files

    def remove_stopwords(self, line):
        return ' '.join([i for i in line.lower().split() if i not in self.stop_words])
