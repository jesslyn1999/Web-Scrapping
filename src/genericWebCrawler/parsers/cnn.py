from bs4 import BeautifulSoup
from spacy.lang.en import English
from src.genericWebCrawler.items import CNNwebcrawlerItem
from src.genericWebCrawler.parsers.generic import GenericParser
import re
import requests
import traceback
import sys

class CNNParser(GenericParser):
    domain_name = "*cnnindonesia.com"

    def __init__(self):
        super().__init__()

    def parser(self, response, keywords):
        # articleid = re.search('(\d+)-(\d+)-(\d+)', response.meta["url"]).group(3)
        # print(f"request for article {articleid}")

        self._item = CNNwebcrawlerItem()
        bsoup = BeautifulSoup(response.body, 'html.parser')
        self._item["Title"] = bsoup.title.string
        self._item["URLNews"] = response.meta["url"]
        self._item["Body"] = []
        self._item["FollowLinks"] = list(
            self.get_all_links(response, keywords))


        try:
            temp_read_time = bsoup.find(
                "div", {"class": "read__time"}).get_text().split('-')
            if len(temp_read_time) == 2:
                self._item["Time"] = temp_read_time[0].strip()
                self._item["Source"] = temp_read_time[1].strip()
            else:
                self._item["Time"] = temp_read_time[0].strip()

            temp_author = bsoup.find("div", {"id": "penulis"}).find("a")
            temp_editor = bsoup.find("div", {"id": "editor"}).find("a")
            self._item["Author"] = {
                "Name": temp_author.get_text(), "URLProfile": temp_author.get('href')}
            self._item["Editor"] = {
                "Name": temp_editor.get_text(), "URLProfile": temp_editor.get('href')}
            # Comment scraping section:
            self._item["Comments"] = []
            try:
                # GraphQL Comment API
                articleId = bsoup.find("meta", {"name": "articleid"})["content"]
                params = """
                { 
                search(type: "comment",size: 10 ,page:1,sort:"newest", adsLabelKanal: "cnn_nasional", adsEnv: "desktop", query: [{name: "news.artikel", terms: "%s" } , {name: "news.site", terms: "cnn"} ]) { 
                    paging 
                    sorting 
                    counter 
                    counterparent 
                    profile 
                    hits { 
                    posisi 
                    hasAds 
                    results { 
                        id 
                        author 
                        content 
                        like 
                        prokontra 
                        status 
                        news 
                        create_date 
                        pilihanredaksi 
                        refer 
                        liker { 
                        id 
                        } 
                        reporter { 
                        id 
                        status_report 
                        } 
                        child { 
                        id 
                        child 
                        parent 
                        author 
                        content 
                        like 
                        prokontra 
                        status 
                        create_date 
                        pilihanredaksi 
                        refer 
                        liker { 
                            id 
                        } 
                        reporter { 
                            id 
                            status_report 
                        } 
                        authorRefer  
                        }  
                    }  
                    }  
                }  
                }""" % articleId

                response_ = requests.get("https://newcomment.detik.com/graphql",
                                params={
                                    "query": params
                                })

                results = response_.json()

            
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
            except Exception as e:
                print("error type: " + str(e))
                print(traceback.format_exc())
            # Comment scraping section end
        except AttributeError:
            pass

        # FILL BODY: for CNN text is located under this id:
        p_children = bsoup.find_all("div", {"id": "detikdetailtext"})

        for p_child in p_children:
            child = p_child.get_text()
            string = child.strip()
            doc = self.nlp(string)
            sentences = [" ".join(sent.string.strip().split())
                         for sent in doc.sents]
            self._item["Body"].extend(sentences)

        return self._item
