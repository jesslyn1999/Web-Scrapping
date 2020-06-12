from bs4 import BeautifulSoup
from genericWebCrawler.genericWebCrawler.parsers.generic import GenericParser
from genericWebCrawler.genericWebCrawler.items import KompaswebcrawlerItem


class KompasParser(GenericParser):
    domain_name = "*kompas.com"

    def __init__(self):
        super().__init__()

    def parser(self, response, keywords):
        bsoup = BeautifulSoup(response.text, "html.parser")
        self._item = KompaswebcrawlerItem()

        self._item["Title"] = bsoup.title.string
        self._item["URLNews"] = response.meta["url"]
        self._item["Body"] = []
        self._item["FollowLinks"] = list(self.get_all_links(response, keywords))

        try:
            temp_read_time = bsoup.find("div", {"class": "read__time"}).get_text().split('-')
            if len(temp_read_time) == 2:
                self._item["Time"] = temp_read_time[0].strip()
                self._item["Source"] = temp_read_time[1].strip()
            else:
                self._item["Time"] = temp_read_time[0].strip()

            temp_author = bsoup.find("div", {"id": "penulis"}).find("a")
            temp_editor = bsoup.find("div", {"id": "editor"}).find("a")
            self._item["Author"] = {"Name": temp_author.get_text(), "URLProfile": temp_author.get('href')}
            self._item["Editor"] = {"Name": temp_editor.get_text(), "URLProfile": temp_editor.get('href')}
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
