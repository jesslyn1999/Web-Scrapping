from bs4 import BeautifulSoup
from src.genericWebCrawler.parsers.generic import GenericParser
from src.genericWebCrawler.items import DetikwebcrawlerItem
import dateparser
import requests
import traceback
import sys


def time_gmt_format(str_datetime):
    # from string like "Senin, 06 Jul 2020 07:02 WIB" to GMT yyyymmddhhmmss
    date_time_obj = dateparser.parse(str_datetime, date_formats=[
                                     '%A, %d %b %Y %H:%M %Z'], settings={'TO_TIMEZONE': 'GMT'})
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
            self._item["Time"] = bsoup.find(
                "div", {"class": "detail__date"}).get_text()
            self._item["StandardTime"] = time_gmt_format(self._item["Time"])

            temp_read_author = bsoup.find(
                "div", {"class": "detail__author"}).get_text().split('-')
            if len(temp_read_author) == 2:
                self._item["Source"] = temp_read_author[0].strip()
                self._item["Time"] = temp_read_author[1].strip()
            else:
                self._item["Source"] = temp_read_author[0].strip()

            # Comment scraping section:
            self._item["Comments"] = []
            self._item["Reactions"] = {}
            try:
                # GraphQL Comment API
                headers = {
                    'authority': 'apicomment.detik.com',
                    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.116 Safari/537.36',
                    'sec-fetch-dest': 'empty',
                    'accept': '*/*',
                    'origin': 'https://newcomment.detik.com',
                    'sec-fetch-site': 'same-site',
                    'sec-fetch-mode': 'cors',
                    'referer': 'https://newcomment.detik.com/static/index.htm?v=1&version=latest&uid=030ed857a6&logLevel=error&xcomponent=1',
                    'accept-language': 'en-US,en;q=0.9',
                    'cookie': '_ga=GA1.2.1456088112.1594021195; __auc=e0779b95173231131281c8f9990; _fbp=fb.1.1594021196383.368542258; comment_token=xcM8MmDEQP2x00AB0DUsXd575VIvB6yAwNSVSmczNE7WBEdT2bTcLqvzryGkZJbl; __asc=78d4d624173b2cbc01fcc6b1855; _gid=GA1.2.1107085298.1596432564; __dtma=146380193.781214540.1594021208.1594021208.1596432565.2; __dtmc=146380193; _hjid=0a202206-3b1d-414f-846d-eca09653c902; __dtmids=5117914,5118071; _hjAbsoluteSessionInProgress=1; __dtmb=146380193.7.10.1596433717',
                }

                articleId = bsoup.find("meta", {"name": "articleid"})[
                    "content"]

                params = """
                { search(type: "comment",size: 10 ,page:2,sort:"newest", adsLabelKanal: "detik_news", adsEnv: "desktop", query: [{name: "news.artikel", terms: "%s" } , {name: "news.site", terms: "dtk"} ]) { paging sorting counter counterparent profile hits { posisi hasAds results { id author content like prokontra status news create_date pilihanredaksi refer liker { id } reporter { id status_report } child { id child parent author content like prokontra status create_date pilihanredaksi refer liker { id } reporter { id status_report } authorRefer  }  }  }  }  }""" % articleId

                comment_response = requests.get("https://apicomment.detik.com/graphql",
                                                params={
                                                    "query": params
                                                }, headers=headers)
                results = comment_response.json()

                commentArray = [t for t in results["data"]
                                ["search"]["hits"]["results"]]

                for comment in commentArray:
                    if(comment["status"] == None):
                        continue
                    temp_dict = {}
                    temp_dict["Author"] = comment['author']['name']
                    temp_dict["Content"] = comment['content']
                    temp_dict["Likes"] = comment['like']
                    self._item["Comments"].append(temp_dict)

                # reaction scraping section
                kanal = bsoup.find("meta", {"name": "kanalid"})[
                    "content"].split('-')
                kanalId = kanal[1]
                subKanalId = kanal[2]

                reaction_params = {
                    "idkanal": kanalId,
                    "idnews": articleId,
                    "idsubkanal": subKanalId,
                    "idfokus": 0,
                    "idmicrosite": 0,
                    "news_url": response.meta["url"]
                }
                reaction_response = requests.get(
                    "https://mood.detik.com/api/init", params=reaction_params)
                reaction_results = reaction_response.json()
                for reaction in reaction_results['result']:
                    self._item["Reactions"][reaction] = reaction_results['result'][reaction]

            except Exception as e:
                print("error type: " + str(e))
                print(traceback.format_exc())
            # Comment scraping section end

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
