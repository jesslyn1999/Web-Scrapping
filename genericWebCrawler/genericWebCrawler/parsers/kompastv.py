from bs4 import BeautifulSoup
from genericWebCrawler.genericWebCrawler.parsers.generic import GenericParser
from genericWebCrawler.genericWebCrawler.items import KompasTvwebcrawlerItem


class KompasTvParser(GenericParser):
    domain_name = "*kompas.tv"

    def __init__(self):
        super().__init__()

    def parser(self, response, keywords):
        bsoup = BeautifulSoup(response.text, "html.parser")
        self._item = KompasTvwebcrawlerItem()

        self._item["Title"] = bsoup.title.string
        self._item["URLNews"] = response.meta["url"]
        self._item["Body"] = []
        self._item["FollowLinks"] = list(self.get_all_links(response, keywords))

        try:
            self._item["Time"] = bsoup.find("span", {"class": "time-news"}).get_text().strip()
            self._item["Editor"] = bsoup.find("span", {"class": "pub"}).get_text()
        except AttributeError:
            pass

        p_children = bsoup.find_all("p")

        for p_child in p_children:
            child = p_child.get_text()
            string = child.strip()
            doc = self.nlp(string)
            sentences = [" ".join(sent.string.strip().split()) for sent in doc.sents]
            self._item["Body"].extend(sentences)

        print('ITEM: ')
        print(self._item)
        return self._item
