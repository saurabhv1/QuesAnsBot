from base_question_processor import BaseQuestionProcessor

class CommandQuestionProcessor(BaseQuestionProcessor):
    def __init__(self, question):
        super(CommandQuestionProcessor, self).__init__(question)

    def process(self):
        return self.find_best_url()

    def find_best_url(self):
        urls_file = '../train/data/urls.txt'
        max_score = -1
        result = ''
        with open(urls_file) as f:
            for line in f:
                url = line.strip()
                clean_url = self.clean_url(url)
                vector1 = self.text_to_vector(clean_url)
                vector2 = self.text_to_vector(self.question)
                cosine = self.get_cosine_score(vector2, vector1)
                if cosine > max_score:
                    max_score = cosine
                    result = url
        return result, max_score

    def clean_url(self, url):
        if not url or len(url) < 1:
            return ''
        res = []
        url = url.replace('http://','').replace('www.', '').replace('.com', '')
        url_words = url.split('/')
        for url_word in url_words:
            res += url_word.split('-')
        return ' '.join(res)