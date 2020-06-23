from bs4 import BeautifulSoup
from src.genericWebCrawler.parsers.generic import GenericParser
from src.genericWebCrawler.items import KompasTvwebcrawlerItem
import dateparser


def time_gmt_format(str_datetime):
    # from string like "Senin, 22 Juni 2020 | 15:30 WIB" to GMT yyyymmddhhmmss
    date_time_obj = dateparser.parse(str_datetime, date_formats=['%A, %d %B %Y | %H:%M %Z'],
                                     settings={'TO_TIMEZONE': 'GMT'})
    return date_time_obj.strftime('%Y%m%d%H%M%S')


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
            self._item["StandardTime"] = time_gmt_format(self._item["Time"])
            self._item["Editor"] = bsoup.find("span", {"class": "pub"}).get_text()
        except AttributeError:
            pass

        p_children = bsoup.find_all("p")

        for p_child in p_children:
            child = p_child.get_text()
            string = child.strip()
            doc = self.nlp(string)
            sentences = [" ".join(sent.string.strip().split()).translate(self.replace_punctuation)
                         for sent in doc.sents]
            self._item["Body"].extend(sentences)

        return self._item
