from scrapy.spiders import Spider
from scrapy import Request
from scrapy.linkextractors import LinkExtractor
from spacy.tokens import Token
from spacy.lang.en import English # updated
from urllib.parse import urlparse
# from w3lib.html import remove_tags
from bs4 import BeautifulSoup
from genericWebCrawler.genericWebCrawler.items import GenericwebcrawlerItem
from genericWebCrawler.genericWebCrawler.parser import parsers

# Faster alternative? :
# from nltk import tokenize
# have to download punkt: python -m nltk.downloader 'punkt' OR go to python shell and type 'nltk.download('punkt')
def create_crawler_class():
    Token.set_extension('tag', default=False)

    results = []

    class UrlExtractor(Spider):
        name = 'url-extractor'
        start_urls = []
        nlp = English()
        nlp.add_pipe(nlp.create_pipe('sentencizer'))

        def __init__(self, root=None, depth=0, *args, **kwargs):
            self.logger.info("[LE] Source: %s Depth: %s Kwargs: %s", root, depth, kwargs)
            self.source = root
            self.options = kwargs
            self.depth = depth
            self.traversedLinks = set()
            UrlExtractor.start_urls.append(root)
            # print(self.options.get('allow_domains'))
            if self.options.get('allow_domains') != '':
                print("allowed domains set to given settings")
            else:
                print("allowed domains set to ROOT DOMAIN: ")
                root_domain = urlparse(root).netloc
                root_domain = '.'.join(root_domain.split('.')[1:])
                self.options['allow_domains'] = root_domain
                # print(self.options.get('allow_domains'))
            UrlExtractor.allowed_domains = [self.options.get('allow_domains')]

            self.clean_options()
            self.le = LinkExtractor(allow=self.options.get('allow'), deny=self.options.get('deny'),
                                    allow_domains=self.options.get('allow_domains'),
                                    deny_domains=self.options.get('deny_domains'),
                                    restrict_xpaths=self.options.get('restrict_xpaths'),
                                    canonicalize=False,
                                    unique=True, process_value=None, deny_extensions=None,
                                    restrict_css=self.options.get('restrict_css'),
                                    strip=True)
            super(UrlExtractor, self).__init__(*args, **kwargs)

        def start_requests(self, *args, **kwargs):
            yield Request('%s' % self.source, callback=self.parse_req, meta={'url': self.source})

        def tag_visible(element):
            if element.parent.name in ['a', 'style', 'script', 'head', 'title', 'meta', '[document]']:
                return False
            if isinstance(element, Comment):  # TODO: WHY Comment UNDEFINED ?
                return False
            return True

        def parse_req(self, response):
            (title, url, listOfSentences, all_urls) = parsers.parse(response.url, response)

            results.append((title, url, listOfSentences, all_urls))
            non_traversed_urls = all_urls.difference(self.traversedLinks)
            self.traversedLinks = self.traversedLinks | all_urls

            if int(response.meta['depth']) < int(self.depth):
                for url in non_traversed_urls:
                    print("Traversing", url)
                    yield Request('%s' % url, callback=self.parse_req, meta={'url': url})
                if len(non_traversed_urls) > 0:
                    for url in non_traversed_urls:
                        yield dict(link=url, url=url, meta=dict(source=self.source, depth=response.meta['depth']))

            item = GenericwebcrawlerItem()
            item['title'] = title
            item['url'] = response.meta['url']
            item['sentences'] = listOfSentences
            item['links'] = list(all_urls)
            yield item

        def get_all_links(self, response):
            links = self.le.extract_links(response)
            str_links = set()
            for link in links:
                if(link.url not in self.traversedLinks):
                    str_links.add(link.url)
            return str_links

        def clean_options(self):
            allowed_options = ['allow', 'deny', 'allow_domains', 'deny_domains', 'restrict_xpaths', 'restrict_css']
            for key in allowed_options:
                if self.options.get(key, None) is None:
                    self.options[key] = []
                else:
                    self.options[key] = self.options.get(key).split(',')

    return results, UrlExtractor
