from bs4 import BeautifulSoup
from genericWebCrawler.genericWebCrawler.parsers.generic import GenericParser
from genericWebCrawler.genericWebCrawler.items import KompaswebcrawlerItem
from spacy.lang.en import English

nlp = English()
nlp.add_pipe(nlp.create_pipe("sentencizer"))


class KompasParser(GenericParser):
    domain_name = "*kompas.com"

    def __init__(self):
        super().__init__()
        self._item = KompaswebcrawlerItem()

    def parser(self, response, keywords):
        bsoup = BeautifulSoup(response.text, "html.parser")

        self._item["Title"] = bsoup.title.string
        self._item["URLNews"] = response.meta["url"]
        self._item["Body"] = []
        self._item["FollowLinks"] = list(self.get_all_links(response, keywords))

        temp_read_time = bsoup.find("div", {"class": "read__time"}).get_text().split('-')
        if len(temp_read_time) == 2 :
            self._item["Time"] = temp_read_time[0].strip()
            self._item["Source"] = temp_read_time[1].strip()
        else:
            self._item["Time"] = temp_read_time[0].strip()

        temp_author = bsoup.find("div", {"id": "penulis"}).find("a")
        temp_editor = bsoup.find("div", {"id": "editor"}).find("a")
        self._item["Author"] = {"Name": temp_author.get_text(), "URLProfile": temp_author.get('href')}
        self._item["Editor"] = {"Name": temp_editor.get_text(), "URLProfile": temp_editor.get('href')}

        p_children = bsoup.find_all("p")

        for p_child in p_children:
            child = p_child.get_text()
            string = child.strip()
            doc = nlp(string)
            sentences = [" ".join(sent.string.strip().split()) for sent in doc.sents]
            self._item["Body"].extend(sentences)
        print("ITEM FOR KOMPAS PARSER: ")
        print(self._item)
        return self._item
