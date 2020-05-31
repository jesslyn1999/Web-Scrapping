from bs4 import BeautifulSoup
from scrapy.linkextractors import LinkExtractor
from spacy.lang.en import English
from genericWebCrawler.genericWebCrawler.items import KompaswebcrawlerItem


nlp = English()
nlp.add_pipe(nlp.create_pipe('sentencizer'))


def kompas_parser(url, response):
    bsoup = BeautifulSoup(response.text, 'html.parser')

    item = KompaswebcrawlerItem()
    item['title'] = bsoup.title.string
    item['url'] = response.meta['url']
    item['sentences'] = []
    item['follow_links'] = list(get_all_links(response))

    p_children = bsoup.find_all('p')

    for p_child in p_children:
        child = p_child.get_text()
        string = child.strip()
        doc = nlp(string)
        sentences = [" ".join(sent.string.strip().split()) for sent in doc.sents]
        item['sentences'].extend(sentences)
    return item


def get_all_links(response):
    le = LinkExtractor(canonicalize=False,
                       unique=True, process_value=None, deny_extensions=None,
                       strip=True)
    links = le.extract_links(response)
    str_links = set()
    for link in links:
        str_links.add(link.url)
    return str_links
