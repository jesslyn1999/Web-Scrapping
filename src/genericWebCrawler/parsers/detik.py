from bs4 import BeautifulSoup
from src.genericWebCrawler.parsers.generic import GenericParser
from src.genericWebCrawler.items import KompaswebcrawlerItem
import requests
import dateparser


def time_gmt_format(str_datetime):
    # from string like "11/06/2020, 13:45 WIB" to GMT yyyymmddhhmmss
    date_time_obj = dateparser.parse(str_datetime, date_formats=['%d/%m/%Y, %H:%M %Z'], settings={'TO_TIMEZONE': 'GMT'})
    return date_time_obj.strftime('%Y%m%d%H%M%S')


class KompasParser(GenericParser):
    domain_name = "*kompas.com"

    def __init__(self):
        super().__init__()

    def parser(self, response, keywords):
        bsoup = BeautifulSoup(response.text, "html.parser")
        # :nbsp; & punctuation & case folding: lowercase
        bsoup.prettify(formatter=lambda s: s.replace(u'\xa0', ' ').lower())

        self._item = KompaswebcrawlerItem()

        self._item["FollowLinks"] = list(
            self.get_all_links(response, keywords))
        self._item["URLNews"] = response.meta["url"]
        self._item["Body"] = []

        try:
            self._item["Title"] = bsoup.find("h1", {"class": "read__title"}).get_text()

            # Comment scraping section:
            self._item["Comments"] = []
            commentAPIURL = "https://apis.kompas.com/api/comment/list"
            r = requests.get(commentAPIURL,
                             params={
                                 "urlpage": response.meta["url"],
                                 "json": "",
                                 "limit": 1000
                             })
            results = r.json()
            commentArray = [t for t in results['result']['komentar']]
            for x in commentArray:
                temp_dict = {}
                temp_dict["Author"] = x['user_fullname']
                temp_dict["Content"] = x['comment_text']
                temp_dict["Likes"] = x['num_like']
                temp_dict['Dislikes'] = x['num_dislike']
                self._item["Comments"].append(temp_dict)
            # Comment scraping section end

            temp_read_time = bsoup.find(
                "div", {"class": "read__time"}).get_text().split('-')
            if len(temp_read_time) == 2:
                self._item["Source"] = temp_read_time[0].strip()
                self._item["Time"] = temp_read_time[1].strip()
            else:
                self._item["Time"] = temp_read_time[0].strip()

            self._item["StandardTime"] = time_gmt_format(self._item["Time"])

            temp_author = bsoup.find("div", {"id": "penulis"}).find("a")
            temp_editor = bsoup.find("div", {"id": "editor"}).find("a")
            self._item["Author"] = {
                "Name": temp_author.get_text(), "URLProfile": temp_author.get('href')}
            self._item["Editor"] = {
                "Name": temp_editor.get_text(), "URLProfile": temp_editor.get('href')}
        except AttributeError:
            pass

        temp_read_content = bsoup.find("div", {"class": "read__content"})
        if temp_read_content:
            p_children = temp_read_content.find_all("p")
            if p_children:
                if not p_children[0].get_text().strip():
                    p_children.pop(0)
                first_child = p_children.pop(0)
                first_child.find("strong").decompose()
                self._item["Body"].append(first_child.get_text().strip().translate(self.replace_punctuation))

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
