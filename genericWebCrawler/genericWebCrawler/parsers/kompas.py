from bs4 import BeautifulSoup
from genericWebCrawler.genericWebCrawler.parsers.generic import GenericParser
from genericWebCrawler.genericWebCrawler.items import KompaswebcrawlerItem

import requests


class KompasParser(GenericParser):
    domain_name = "*kompas.com"

    def __init__(self):
        super().__init__()

    def parser(self, response, keywords):
        bsoup = BeautifulSoup(response.text, "html.parser")
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
                first_child = p_children.pop(0)
                first_child.find("strong").decompose()
                self._item["Body"].append(first_child.get_text().replace("-", "").strip())

            for p_child in p_children:
                child = p_child.get_text()
                if "Baca juga" in child:
                    continue
                string = child.strip()
                doc = self.nlp(string)
                sentences = [" ".join(sent.string.strip().split())
                             for sent in doc.sents]
                self._item["Body"].extend(sentences)

        return self._item
