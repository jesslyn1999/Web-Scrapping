from bs4 import BeautifulSoup
from genericWebCrawler.genericWebCrawler.parsers.generic import GenericParser
from genericWebCrawler.genericWebCrawler.items import KontanwebcrawlerItem
import re


class KontanParser(GenericParser):
    domain_name = "*kontan.co.id"

    def __init__(self):
        super().__init__()

    def parser(self, response, keywords):
        bsoup = BeautifulSoup(response.text, "html.parser")
        self._item = KontanwebcrawlerItem()

        self._item["Title"] = bsoup.title.string
        self._item["URLNews"] = response.meta["url"]
        self._item["Body"] = []
        self._item["FollowLinks"] = list(self.get_all_links(response, keywords))

        try:
            self._item["Time"] = bsoup.find("div", {"class": "fs14 ff-opensans font-gray"}).get_text().strip()
            temp_list_first_p = bsoup.find("div", {"itemprop": "articleBody"}).find("p").contents
            temp_list = [re.sub(r"[:|\n]|<\s*b[^>]*>|<\s*/\s*b>", "", str(tag)).strip()
                         for tag in temp_list_first_p]
            self._item["Source"] = {}
            for key, value in zip(temp_list[0::2], temp_list[1::2]):
                self._item["Source"][key] = value
        except AttributeError as exc:
            print('err: ', exc)
            pass

        p_children = bsoup.find_all("p")

        for p_child in p_children:
            child = p_child.get_text()
            string = child.strip()
            doc = self.nlp(string)
            sentences = [" ".join(sent.string.strip().split()) for sent in doc.sents]
            self._item["Body"].extend(sentences)

        return self._item
