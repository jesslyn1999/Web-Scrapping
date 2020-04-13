from scrapy.spiders import Spider
from scrapy import Request
from scrapy.linkextractors import LinkExtractor
from spacy.tokens import Token
from spacy.lang.en import English # updated

def create_crawler_class():
    Token.set_extension('tag', default=False)

    results = []

    class UrlExtractor(Spider):
        name = 'url-extractor'
        start_urls = []
        index = 0
        nlp = English()
        nlp.add_pipe(nlp.create_pipe('sentencizer'))

        def __init__(self, root=None, depth=0, *args, **kwargs):
            self.logger.info("[LE] Source: %s Depth: %s Kwargs: %s", root, depth, kwargs)
            self.source = root
            self.options = kwargs
            self.depth = depth
            UrlExtractor.start_urls.append(root)
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

        def parse_req(self, response):
            # see request result
            # print("THE URL: ", response.url)
            title = response.xpath('//title//text()').extract()[0].strip()

            self.index += 1
            # select all texts between tags except script tags:
            temp = response.xpath('//*[not(self::script)]/text()[re:test(., "\w+")]').extract()

            listOfSentences = []
            for string in temp:
                doc = self.nlp(string)
                sentences = [sent.string.strip() for sent in doc.sents]
                listOfSentences.extend(sentences)

            # accumulate result:
            results.append((title, response.meta['url'], listOfSentences))

            all_urls = []
            if int(response.meta['depth']) <= int(self.depth):
                all_urls = self.get_all_links(response)
                for url in all_urls:
                    yield Request('%s' % url, callback=self.parse_req, meta={'url': url})
            if len(all_urls) > 0:
                for url in all_urls:
                    yield dict(link=url, meta=dict(source=self.source, depth=response.meta['depth']))

        def get_all_links(self, response):
            links = self.le.extract_links(response)
            str_links = []
            for link in links:
                str_links.append(link.url)
            return str_links

        def clean_options(self):
            allowed_options = ['allow', 'deny', 'allow_domains', 'deny_domains', 'restrict_xpaths', 'restrict_css']
            for key in allowed_options:
                if self.options.get(key, None) is None:
                    self.options[key] = []
                else:
                    self.options[key] = self.options.get(key).split(',')

    return (results, UrlExtractor)
