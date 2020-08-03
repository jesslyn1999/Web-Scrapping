from bs4 import BeautifulSoup
from src.genericWebCrawler.parsers.generic import GenericParser
from src.genericWebCrawler.items import KompasianawebcrawlerItem
import unicodedata
import requests
import dateparser
import traceback
import sys

def time_gmt_format(str_datetime):
    # from string like "29 Mei 2020   09:00" to GMT yyyymmddhhmmss
    date_time_obj = dateparser.parse(str_datetime, date_formats=['%d %B %Y  %H:%M'],
                                     settings={'TO_TIMEZONE': 'GMT'})
    return date_time_obj.strftime('%Y%m%d%H%M%S')


class KompasianaParser(GenericParser):
    domain_name = "*kompasiana.com"

    def __init__(self):
        super().__init__()

    def parser(self, response, keywords):
        bsoup = BeautifulSoup(response.text, "html.parser")
        self._item = KompasianawebcrawlerItem()

        self._item["Title"] = bsoup.title.string
        self._item["URLNews"] = response.meta["url"]
        self._item["Body"] = []
        self._item["FollowLinks"] = list(
            self.get_all_links(response, keywords))

        try:
            temp_header = bsoup.find(
                "div", {"class": "read-count mt10 mb20 clearfix"})
            span_elements = temp_header.find_all("span")

            self._item["CreatedTime"] = unicodedata.normalize(
                "NFKD", span_elements[0].get_text()).strip()
            self._item["LastEdit"] = unicodedata.normalize("NFKD", span_elements[1].get_text())\
                .replace("Diperbarui:", "").strip()

            self._item["StandardCreatedTime"] = time_gmt_format(self._item["CreatedTime"])
            self._item["StandardLastEditTime"] = time_gmt_format(self._item["LastEdit"])

            self._item["LastSeenNumber"] = temp_header.find(
                "span", {"id": "post-counter"}).get_text()
            self._item["LikeNumber"] = temp_header.find(
                "span", {"id": "post-rate"}).get_text()
            self._item["CommentNumber"] = temp_header.find(
                "span", {"id": "post-comment"}).get_text()
        except AttributeError:
            pass

        
        self._item["Comments"] = []
        # Comment scraping section:
        try:
            # Kompasiana Custom Comment API
            commentAPIURL = "https://www.kompasiana.com/ajax/load_more_comments/"
            # headers are mandatory for kompasiana
            headers = {
                'authority': 'www.kompasiana.com',
                'pragma': 'no-cache',
                'cache-control': 'no-cache',
                'accept': 'application/json, text/javascript, */*; q=0.01',
                'sec-fetch-dest': 'empty',
                'x-requested-with': 'XMLHttpRequest',
                'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.116 Safari/537.36',
                'sec-fetch-site': 'same-origin',
                'sec-fetch-mode': 'cors',
                'referer': 'https://www.kompasiana.com/dodimulyana/5ee1d35c097f362dcf5a9132/ganjar-melawan-megawati-perjanjian-batu-tulis-kembali-terancam',
                'accept-language': 'en-US,en;q=0.9',
                'cookie': 'publica_session_id=7be8b909-7595-c597-23fc-ffd550839d86; k124951894=k124951894; ukid=b9f9c3ee10a0cfe37fa22158e4628ce5; _ga=GA1.2.1534611824.1592201035; _gid=GA1.2.1418603594.1592201035; __asc=a137e7e3172b693bf005f2573d8; __auc=a137e7e3172b693bf005f2573d8; _gaexp=GAX1.2.emxowUjBQFyKHvvjKtNbbA.18517.x474; forkrtg={"generic":"29112019"}; AMP_TOKEN=%24NOT_FOUND; publica_user_id=b73b8cf0-29ec-4456-a653-54aa79a9da84; __gads=ID=dec3797e02d77cba:T=1592201041:S=ALNI_MZykgtlmgyRk2yCZ1uBphFB_yKC8g; OB-USER-TOKEN=73357436-69c1-4bc9-a08b-73f96e3ad304; fmguid={"id":"1dGnWQH8FPRl1lcNnunMsTf1kdK","cat":{"l1":{"1":"c15","2":"c3"},"l2":{"1":"c15","2":"c3"}}}; _gat_UA-3296578-31=1',
            }
            metadata = bsoup.find("div", {"id": "id_post"})

            if metadata:
                post_id = metadata["data-id"]
                post_channel_id = metadata["data-recipientid"]
                params = (
                    ('post_id', post_id),
                    ('post_channel_id', post_channel_id),
                    ('page', '1'),
                    ('per_page', '1000'),
                )
                r = requests.get(commentAPIURL, headers=headers, params=params)
                results = r.json()
                # results are in form of HTML elements for kompasiana
                commentElement = results['view']
                bsoupComment = BeautifulSoup(commentElement, "html.parser")
                commentDivs = bsoupComment.findAll("div", {
                    "class": "komentar-content"
                })
                for div in commentDivs:
                    tempdict = {}
                    # fill comments author
                    h1User = div.find("h1", {
                        "class": "komentar-user"
                    })
                    username = h1User.findChildren("a", recursive=False)[0]
                    tempdict["Author"] = username.getText()
                    # fill comments content
                    contentP = div.find("p", {
                        "class": "komentar-text"
                    })
                    tempdict["Content"] = contentP.getText()
                    # fill comments likes
                    likeSpan = div.find("span", {
                        "id": "like-counter"
                    })
                    try:
                        tempdict["Likes"] = likeSpan.getText()
                    except:
                        tempdict["Likes"] = 0
                    self._item["Comments"].append(tempdict)
        except Exception as e:
            print("error type: " + str(e))
            print(traceback.format_exc())
        # Comment scraping section end

        p_children = bsoup.find_all("p")

        for p_child in p_children:
            child = p_child.get_text()
            string = child.strip()
            doc = self.nlp(string)
            sentences = [" ".join(sent.string.strip().split()).translate(self.replace_punctuation)
                         for sent in doc.sents]
            self._item["Body"].extend(sentences)

        return self._item
