from itertools import chain

class QuestionType(object):
    QUESTION_YES_NO     = 'question_yes_no'
    QUESTION_COMMAND    = 'question_command'
    QUESTION_DURATION   = 'question_duration'
    QUESTION_DISTANCE   = 'question_distance'
    QUESTION_COUNT      = 'question_count'

DURATION_KEYWORDS = set(['time', 'how long', 'duration', 'minutes', 
                    'minute', 'min', 'min','min', 'hours', 'hour', 'seconds', 'second', 'sec '])

DISTANCE_KEYWORDS = set(['distance', 'meters', 'meter', 'km', 'kilometers', 'kilometer'])

COUNT_KEYWORDS = set(['how many ', 'what is number ', 'what is the number '])

ALL_KEYWORDS = set(chain(DURATION_KEYWORDS, DISTANCE_KEYWORDS, COUNT_KEYWORDS))
