from bs4 import BeautifulSoup
from genericWebCrawler.genericWebCrawler.parsers.generic import GenericParser
from genericWebCrawler.genericWebCrawler.items import KompasianawebcrawlerItem
import unicodedata


class KompasianaParser(GenericParser):
    domain_name = "*kompasiana.com"

    def __init__(self):
        super().__init__()

    def parser(self, response, keywords):
        bsoup = BeautifulSoup(response.text, "html.parser")
        self._item = KompasianawebcrawlerItem()

        self._item["Title"] = bsoup.title.string
        self._item["URLNews"] = response.meta["url"]
        self._item["Body"] = []
        self._item["FollowLinks"] = list(self.get_all_links(response, keywords))

        try:
            temp_header = bsoup.find("div", {"class": "read-count mt10 mb20 clearfix"})
            span_elements = temp_header.find_all("span")

            self._item["CreatedTime"] = unicodedata.normalize("NFKD", span_elements[0].get_text()).strip()
            self._item["LastEdit"] = unicodedata.normalize("NFKD", span_elements[1].get_text())\
                .replace("Diperbarui:", "").strip()

            self._item["LastSeenNumber"] = temp_header.find("span", {"id": "post-counter"}).get_text()
            self._item["LikeNumber"] = temp_header.find("span", {"id": "post-rate"}).get_text()
            self._item["CommentNumber"] = temp_header.find("span", {"id": "post-comment"}).get_text()
        except AttributeError:
            pass

        p_children = bsoup.find_all("p")

        for p_child in p_children:
            child = p_child.get_text()
            string = child.strip()
            doc = self.nlp(string)
            sentences = [" ".join(sent.string.strip().split()) for sent in doc.sents]
            self._item["Body"].extend(sentences)

        return self._item
