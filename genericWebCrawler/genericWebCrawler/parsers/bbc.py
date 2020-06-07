from genericWebCrawler.genericWebCrawler.parsers.generic import GenericParser
from genericWebCrawler.genericWebCrawler.items import BbcwebcrawlerItem


class BbcParser(GenericParser):
    domain_name = '*bbc.com'

    def __init__(self):
        super().__init__()
        self._item = BbcwebcrawlerItem()


# def bbc_parser(url, response, keywords):
#     bsoup = BeautifulSoup(response.text, 'html.parser')
#
#     item = BbcwebcrawlerItem()
#     item['title'] = bsoup.title.string
#     item['url'] = response.meta['url']
#     item['sentences'] = []
#     item['follow_links'] = list(get_all_links(response, keywords))
#
#     p_children = bsoup.find_all('p')
#
#     for p_child in p_children:
#         child = p_child.get_text()
#         string = child.strip()
#         doc = nlp(string)
#         sentences = [" ".join(sent.string.strip().split()) for sent in doc.sents]
#         item['sentences'].extend(sentences)
#
#     return item
