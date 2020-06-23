from bs4 import BeautifulSoup
from src.genericWebCrawler.parsers.generic import GenericParser
from src.genericWebCrawler.items import KontanwebcrawlerItem
import re
import dateparser


def time_gmt_format(str_datetime):
    # from string like "Selasa, 23 Juni 2020 / 07:10 WIB" to GMT yyyymmddhhmmss
    date_time_obj = dateparser.parse(str_datetime, date_formats=['%A, %d %B %Y / %H:%M %Z'],
                                     settings={'TO_TIMEZONE': 'GMT'})
    return date_time_obj.strftime('%Y%m%d%H%M%S')


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
            self._item["StandardTime"] = time_gmt_format(self._item["Time"])

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
            sentences = [" ".join(sent.string.strip().split()).translate(self.replace_punctuation)
                         for sent in doc.sents]
            self._item["Body"].extend(sentences)

        return self._item
