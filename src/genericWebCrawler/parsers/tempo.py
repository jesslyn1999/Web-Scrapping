from bs4 import BeautifulSoup
from src.genericWebCrawler.parsers.generic import GenericParser
from src.genericWebCrawler.items import TempowebcrawlerItem
import requests
import dateparser
import json
import traceback
import sys

FACEBOOK_GRAPH_API_ACCESS_TOKEN = "EAALSGqipwgUBAJp8sgrOwxNZClmCqaxJl8Yu206ZAZAQ4B4ytGY9mvrUqsQZAhXfiWFvKjUM9gA53AIJ65tVBcvW1jZANRAhCkZAZBZCRoWzxmDdeGlWYYVUilZCMNijxhD7X4XZBvwdmZCjilPpGFAyA1PDZCIHwPBuJRA1Sgblvnhy7QZDZD"

def time_gmt_format(str_datetime):
    # from string like "2020-07-03T20:31:24+07:00" to GMT yyyymmddhhmmss
    date_time_obj = dateparser.parse(
        str_datetime, settings={'TO_TIMEZONE': 'GMT'})
    return date_time_obj.strftime('%Y%m%d%H%M%S')


class TempoParser(GenericParser):
    domain_name = "*tempo.co"

    def __init__(self):
        super().__init__()

    def parser(self, response, keywords):
        bsoup = BeautifulSoup(response.text, "html.parser")
        # :nbsp; & punctuation & case folding: lowercase
        bsoup.prettify(formatter=lambda s: s.replace(u'\xa0', ' ').lower())

        temp_content_json = json.loads(bsoup.find(
            "script", type="application/ld+json").string)
        self._item = TempowebcrawlerItem()

        self._item["FollowLinks"] = list(
            self.get_all_links(response, keywords))
        self._item["URLNews"] = response.meta["url"]
        self._item["Body"] = []

        # comment scraping section:
        self._item["Comments"] = []
        try:
            # Facebook Comment API
            articleURL = bsoup.find('link', {"rel": "original-source"})["href"]

            r = requests.get("https://graph.facebook.com/v2.6/",
                            params={
                                "fields": "og_object{comments}",
                                "id": "https://gaya.tempo.co/read/1361609/ramai-kalung-antivirus-corona-cek-harganya-di-pasaran",
                                "access_token": FACEBOOK_GRAPH_API_ACCESS_TOKEN
                            })
            results = r.json()

            try:   
                data = results["og_object"]["comments"]["data"]
                for comment in data:
                    temp_dict = {}
                    temp_dict["Name"] = comment['from']['name']
                    temp_dict["Content"] = comment['message']
                    temp_dict["Date"] = time_gmt_format(comment['created_time'])
                    self._item["Comments"].append(temp_dict)
            except AttributeError as e:
                print(e)
        except Exception as e:
            print("error type: " + str(e))
            print(traceback.format_exc())
        # Comment scraping section end
        
        try:
            self._item["Title"] = temp_content_json["headline"]
            self._item["Source"] = temp_content_json["publisher"]["name"]
            self._item["Time"] = temp_content_json["datePublished"]
            self._item["TimeModified"] = temp_content_json["dateModified"]
            self._item["Author"] = temp_content_json["author"]["name"]
            self._item["Editor"] = temp_content_json["editor"]["name"]
            self._item["Description"] = temp_content_json["description"]
            self._item["StandardTime"] = time_gmt_format(self._item["Time"])
            self._item["Body"].append(temp_content_json["articleBody"].split('-', 1)[-1]
                                      .strip().translate(self.replace_punctuation))
        except AttributeError:
            pass
        return self._item
