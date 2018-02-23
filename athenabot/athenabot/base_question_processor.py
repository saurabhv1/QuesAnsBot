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
        self.question = question
        self.stop_words = set(stopwords.words('english'))
        self.word_pattern = re.compile(r'\w+')
        self.tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')

    def process(self, keywords = [], clean_sentence=False, number_present=False):
        data_dir = '../train/data/' if len(keywords) == 0 else '../train/data_kw/'
        return self.get_best_sentence_match(keywords, clean_sentence, number_present, data_dir)

    def get_best_sentence_match(self, keywords, clean_sentence, number_present, data_dir):
        max_score = -1
        result = ''
        all_files = self.get_all_files()
        for count, file in enumerate(all_files):
            file = data_dir + file
            file_content = open(file).read()
            sentences = self.get_sentences(file_content, file)
            for sentence in sentences:
                cleaned_sentence, words = self.clean_sentence(sentence, file)
                if len(keywords) > 0 and not any(keyword in words for keyword in keywords):
                    continue
                #if file.endswith('athenaclinicalsehr.txt'):# and '106' in cleaned_sentence:
                #    import pdb; pdb.set_trace()
                if number_present and not any(is_number(word) for word in words):
                    continue
                vector1 = self.text_to_vector(cleaned_sentence)
                vector2 = self.text_to_vector(self.question)
                cosine = self.get_cosine_score(vector2, vector1)
                if cosine > max_score:
                    max_score = cosine
                    result = sentence


                '''
                all_words = sentence.split()
                total_words = len(all_words)
                for pos, word in enumerate(all_words):
                    #if word == 'minutes' and file.endswith('athenahealthcominsightwhat-doctors-want-more-time-patients.txt'):
                    #    import pdb; pdb.set_trace()
                    word = self.clean_word(word)
                    #word = self.remove_stopwords(word)
                    if len(keywords) > 0 and word in keywords:
                        previous_sentence = self.get_previous_words(all_words, pos)
                        next_sentence = self.get_next_words(all_words, pos, total_words)
                        for sentence in [previous_sentence, next_sentence]:
                            vector1 = self.text_to_vector(sentence)
                            vector2 = self.text_to_vector(self.question)
                            cosine = self.get_cosine_score(vector2, vector1)
                            if cosine > max_score:
                                max_score = cosine
                                result = sentence
                '''
        #result = self.clean_result(result)
        return result, max_score

    '''
    def clean_word(self, word):
        word = self.remove_stopwords(word)
        match = re.match(r"([0-9]+)([a-z]+)", word, re.I) # for cases like 20times
        if match:
            return match.groups()[1]
        else:
            return word
    '''

    def clean_sentence(self, sentence, file):
        final_words = []
        #if file.endswith('athenaclinicalsehr.txt') and '106' in sentence:
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
        #if file.endswith('athenaclinicalsehr.txt'):
        #    import pdb; pdb.set_trace()
        temp = content.replace('. ', '||').replace('*', '||').replace(':', '||').replace(' ', '||')
        words = temp.split('||')
        cur_words = []
        for word in words:
            if self.is_sentence_breaker(word):
                res.append(' '.join(cur_words))
                cur_words = []
            else:
                cur_words.append(word)
        return res

    def is_sentence_breaker(self, word):
        if re.match(r"([0-9]+),([0-9]+)", word, re.I): # for cases like 200,00
            return False
        elif re.match(r"([0-9]+),%", word, re.I): # for cases like 20%
            return False
        if not word.isalnum() :
            return True
        return False

    def get_previous_words(self, words, cur_pos, count=10):
        previous_pos = max(0, cur_pos-count)
        return ' '.join(words[previous_pos: cur_pos+1])

    def get_next_words(self, words, cur_pos, total_words, count=10):
        next_pos = min(total_words-1, cur_pos+count)
        return ' '.join(words[cur_pos-1: next_pos+1])

    def get_previous_next_words(self, content, cur_pos, total_words, count=5):
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
        data_dir = '../train/data'
        all_files = [f for f in os.listdir(data_dir) if not(f == 'urls.txt')]
        return all_files

    def remove_stopwords(self, line):
        return ' '.join([i for i in line.lower().split() if i not in self.stop_words])
