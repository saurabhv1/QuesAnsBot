from constants import QuestionType, DURATION_KEYWORDS, DISTANCE_KEYWORDS, COUNT_KEYWORDS
import nltk

class QuestionParser(object):
    def __init__(self, question):
        self.question = question.lower().strip()
        self.question_words = nltk.word_tokenize(self.question)
        self.pos_tags = nltk.pos_tag(self.question_words)

        self.question_class_function_dict = [   (QuestionType.QUESTION_YES_NO,      self.is_question_yes_no),
                                                (QuestionType.QUESTION_COMMAND,     self.is_question_command),
                                                (QuestionType.QUESTION_DURATION,    self.is_question_duration),
                                                (QuestionType.QUESTION_DISTANCE,    self.is_question_distance),
                                                (QuestionType.QUESTION_COUNT,       self.is_question_count)
                                            ]

    def get_question_type(self):
        for question_class, function in self.question_class_function_dict:
            if function():
                return question_class
        return None

    def is_question_yes_no(self):
        keywords = ('is ', 'are ')
        return self.question.startswith(keywords)

    def is_question_command(self):
        return self.pos_tags[0][1] == 'VB' # verb, base form

    def is_question_duration(self):
        return any(keyword in self.question for keyword in DURATION_KEYWORDS)

    def is_question_distance(self):
        return any(keyword in self.question for keyword in DISTANCE_KEYWORDS)

    def is_question_count(self):
        return any(keyword in self.question for keyword in COUNT_KEYWORDS)
        