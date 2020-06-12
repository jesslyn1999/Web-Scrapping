from scrapy.spiders import Spider
from scrapy import Request
from scrapy.linkextractors import LinkExtractor
from spacy.tokens import Token
from spacy.lang.en import English
from urllib.parse import urlparse
from genericWebCrawler.genericWebCrawler.items import GenericwebcrawlerItem
from genericWebCrawler.genericWebCrawler.spiders import crawler


def create_crawler_class():
    Token.set_extension("tag", default=False)
    result = {}

    class UrlExtractor(Spider):
        name = "url-extractor"
        start_urls = []
        nlp = English()
        nlp.add_pipe(nlp.create_pipe("sentencizer"))

        def __init__(self, root=None, depth=0, *args, **kwargs):
            self.logger.info("[LE] Source: %s Depth: %s Args : %s Kwargs: %s", root, depth, args, kwargs)
            self.options = kwargs
            self.depth = depth
            self.traversedLinks = set()
            if isinstance(root, (list, tuple, set)):
                self.start_urls = root
            else:
                self.start_urls.append(root)

            if self.options.get("allow_domains") is None:
                self.options["allow_domains"] = set()
                for root_url in self.start_urls:
                    parsed_uri = urlparse(root_url)
                    self.options["allow_domains"].add('{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri))
            print("Allow domains: ", self.options.get("allow_domains"))

            self.clean_options()
            self.le = LinkExtractor(allow=self.options.get("allow"), deny=self.options.get("deny"),
                                    allow_domains=self.options.get("allow_domains"),
                                    deny_domains=self.options.get("deny_domains"),
                                    restrict_xpaths=self.options.get("restrict_xpaths"),
                                    canonicalize=False,
                                    unique=True, process_value=None, deny_extensions=None,
                                    restrict_css=self.options.get("restrict_css"),
                                    strip=True)
            super(UrlExtractor, self).__init__(*args, **kwargs)

        def start_requests(self, *args, **kwargs):
            for start_url in self.start_urls:
                yield Request("%s" % start_url, callback=self.parse_req,
                              meta={"url": start_url, "parent_url": start_url})

        def parse_req(self, response):
            # initial scrape -> must be scraped no matter what(serves as
            # a starting ground), even if don"t follow keyword!
            item = crawler.parserHelper.parse(response)
            all_urls = set(item["FollowLinks"])

            non_traversed_urls = all_urls.difference(self.traversedLinks)

            self.traversedLinks = self.traversedLinks | all_urls
            if int(response.meta["depth"]) < int(self.depth):
                for url in non_traversed_urls:
                    print("Traversing", url)
                    yield Request("%s" % url, callback=self.parse_req,
                                  meta={"url": url, "parent_url": response.meta["parent_url"]})
                # These functions below seem to be useless
                # if len(non_traversed_urls) > 0:
                #     for url in non_traversed_urls:
                #         yield dict(link=url, url=url, meta=dict(source=self.source, depth=response.meta["depth"]))

            if not response.meta["parent_url"] in result:
                result[response.meta["parent_url"]] = []
            result[response.meta["parent_url"]].append(item)
            if type(item) is GenericwebcrawlerItem:
                print('Urls haven\'t yet to be specifically handled: %s' % item['URLNews'])
            yield item

        def clean_options(self):
            allowed_options = ["allow", "deny", "allow_domains", "deny_domains", "restrict_xpaths", "restrict_css"]
            for key in allowed_options:
                if self.options.get(key, None) is None:
                    self.options[key] = []
                else:
                    if isinstance(self.options.get(key), str):
                        self.options[key] = self.options.get(key).split(",")

        def parse(self, response):
            pass

    return UrlExtractor, result
