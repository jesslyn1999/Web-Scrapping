from bs4 import BeautifulSoup
from spacy.lang.en import English
from genericWebCrawler.genericWebCrawler.items import CNNwebcrawlerItem
from genericWebCrawler.genericWebCrawler.parsers.get_all_links import get_all_links
import dryscrape
nlp = English()
nlp.add_pipe(nlp.create_pipe('sentencizer'))


def cnn_parser(url, response, keywords):
    session = dryscrape.Session()
    session.visit(my_url)
    response = session.body()
    bsoup = BeautifulSoup(response.text, 'html.parser')
    print('----------------------------------------------------------------------------------------')
    # print(bsoup.prettify())
    x = bsoup.findAll("div", {"class": "comment__cmt_box_text___3bK3O comment__cmt_dk_komen___1Yzyg"})
    print(x)

    item = CNNwebcrawlerItem()
    item['title'] = bsoup.title.string
    item['url'] = response.meta['url']
    item['sentences'] = []
    item['follow_links'] = list(get_all_links(response, keywords))

    p_children = bsoup.find_all('p')

    for p_child in p_children:
        child = p_child.get_text()
        string = child.strip()
        doc = nlp(string)
        sentences = [" ".join(sent.string.strip().split()) for sent in doc.sents]
        item['sentences'].extend(sentences)
    return item



