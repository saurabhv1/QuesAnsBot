from bs4 import BeautifulSoup, SoupStrainer
from bs4.element import Comment
#import urllib.request
import requests
from urllib2 import urlopen
import os


class TrainService(object):
    def __init__(self, urllist):
        '''
        cmd = 'mkdir data'
        os.system(cmd)
        cwd = os.getcwd()
        url_file = cwd + '/data/urls.txt'
        self.urls_file = open(url_file, 'w')

        self.all_urls = []
        for url in urllist:
            self.all_urls += self.get_all_links(url)
        self.urls_file.close()
        import pdb; pdb.set_trace()
        '''
        #fixed_urls = ['https://www.athenahealth.com/insight/what-doctors-want-more-time-patients']
        #self.all_urls += fixed_urls            
        #self.page_content = []
        pass

    def tag_visible(self, element):
        if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
            return False
        if isinstance(element, Comment):
            return False
        return True

    def text_from_html(self, body):
        soup = BeautifulSoup(body, 'html.parser')
        texts = soup.findAll(text=True)
        visible_texts = filter(self.tag_visible, texts)  
        return u" ".join(t.strip() for t in visible_texts)

    def process(self):
        with open('./data/urls.txt') as f:
            for url in f:
                url = url.strip()
                url_name = url.replace('/', '').replace('www','').replace('https:', '').replace('.', '')
                outfile = './data/' + url_name + '.txt'
                f_out = open(outfile, 'wb')
                try:
                    html = requests.get(url).content
                except:
                    continue
                content = self.text_from_html(html)
                content = url + '\n' + content
                f_out.write(content.encode('UTF-8'))
                f_out.close()
                #self.page_content.append(content)

    def get_all_links(self, url):
        links = set()
        html = urlopen(url).read()
        #import pdb; pdb.set_trace()
        html = requests.get(url).content
        for link in BeautifulSoup(html, parseOnlyThese=SoupStrainer('a')):
            if link.has_attr('href'):
                full_url = self.get_full_url(link['href'], url)
                if full_url in links:
                    continue
                links.add(full_url)
                try:
                    print len(links),full_url
                    self.urls_file.write(full_url + '\n')
                except:
                    continue
                # Go 1 level deep
                html_depth1 = requests.get(url).content
                for nested_link in BeautifulSoup(html_depth1, parseOnlyThese=SoupStrainer('a')):
                    if nested_link.has_attr('href'):
                        full_url = self.get_full_url(link['href'], url)
                        if full_url in links:
                            continue
                        links.add(full_url)
                        try:
                            print len(links), full_url
                            self.urls_file.write(full_url + '\n')
                        except:
                            continue
        return links

    def get_full_url(self, url, parent_url):
        if url.startswith('http'):
            return url
        elif url.startswith('/'):
            return 'https://www.athenahealth.com' + url
        else:
            return parent_url + url
        
        
if __name__ == '__main__':
    urls = ['https://www.athenahealth.com/', 'https://www.athenahealth.com/insight/']
    obj = TrainService(urls)
    obj.process()
