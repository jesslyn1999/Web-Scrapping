from bs4 import BeautifulSoup
from src.genericWebCrawler.parsers.generic import GenericParser
from src.genericWebCrawler.items import DetikwebcrawlerItem
import dateparser


def time_gmt_format(str_datetime):
    # from string like "Senin, 06 Jul 2020 07:02 WIB" to GMT yyyymmddhhmmss
    date_time_obj = dateparser.parse(str_datetime, date_formats=['%A, %d %b %Y %H:%M %Z'], settings={'TO_TIMEZONE': 'GMT'})
    return date_time_obj.strftime('%Y%m%d%H%M%S')


class DetikParser(GenericParser):
    domain_name = "*detik.com"

    def __init__(self):
        super().__init__()

    def parser(self, response, keywords):
        bsoup = BeautifulSoup(response.text, "html.parser")
        # :nbsp; & punctuation & case folding: lowercase
        bsoup.prettify(formatter=lambda s: s.replace(u'\xa0', ' ').lower())

        self._item = DetikwebcrawlerItem()

        self._item["Title"] = bsoup.title.string
        self._item["FollowLinks"] = list(
            self.get_all_links(response, keywords))
        self._item["URLNews"] = response.meta["url"]
        self._item["Body"] = []

        try:
            self._item["Time"] = bsoup.find("div", {"class": "detail__date"}).get_text()
            self._item["StandardTime"] = time_gmt_format(self._item["Time"])

            temp_read_author = bsoup.find(
                "div", {"class": "detail__author"}).get_text().split('-')
            if len(temp_read_author) == 2:
                self._item["Source"] = temp_read_author[0].strip()
                self._item["Time"] = temp_read_author[1].strip()
            else:
                self._item["Source"] = temp_read_author[0].strip()
        except AttributeError:
            pass

        temp_read_content = bsoup.find("div", {"class": "detail__body-text"})
        if temp_read_content:
            p_children = temp_read_content.find_all("p")
            for p_child in p_children:
                child = p_child.get_text()
                if "Baca juga" in child or not p_child.get_text().strip():
                    continue
                string = child.strip()
                doc = self.nlp(string)
                sentences = [" ".join(sent.string.strip().split()).translate(self.replace_punctuation)
                             for sent in doc.sents]
                self._item["Body"].extend(sentences)

        return self._item
