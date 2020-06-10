import re
from bs4 import BeautifulSoup
from scrapy.linkextractors import LinkExtractor
from spacy.lang.en import English
from genericWebCrawler.genericWebCrawler.items import GenericwebcrawlerItem

nlp = English()
nlp.add_pipe(nlp.create_pipe('sentencizer'))


class GenericParser(object):
    domain_name = '*'

    def __init__(self):
        self._item = GenericwebcrawlerItem()

    def parser(self, response, keywords):
        bsoup = BeautifulSoup(response.text, 'html.parser')

        self._item['Title'] = bsoup.title.string
        self._item['URLNews'] = response.meta['url']
        self._item['Body'] = []
        self._item['FollowLinks'] = list(self.get_all_links(response, keywords))

        p_children = bsoup.find_all('p')

        for p_child in p_children:
            child = p_child.get_text()
            string = child.strip()
            doc = nlp(string)
            sentences = [" ".join(sent.string.strip().split()) for sent in doc.sents]
            self._item['Body'].extend(sentences)
        return self._item

    @staticmethod
    def get_all_links(response, keywords):  # 'keywords' is an array of keyword strings
        le = LinkExtractor(canonicalize=False,
                           unique=True, process_value=None, deny_extensions=None,
                           strip=True)
        links = le.extract_links(response)
        str_links = set()
        keywords = keywords.split(',')
        print("keywords", keywords)
        for link in links:
            found = False
            for keyword in keywords:
                if re.search(r"\b%s\b" % re.escape(keyword), link.url):
                    # print("url '%s' contains keyword '%s'" % (link.url, keyword))
                    found = True
                    break
            if found:
                str_links.add(link.url)

        return str_links
