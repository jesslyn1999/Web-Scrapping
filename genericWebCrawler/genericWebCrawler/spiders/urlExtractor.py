from scrapy.spiders import Spider
from scrapy import Request
from scrapy.linkextractors import LinkExtractor
from spacy.tokens import Token
from spacy.lang.en import English # updated
from urllib.parse import urlparse
# from w3lib.html import remove_tags
from bs4 import BeautifulSoup
from genericWebCrawler.genericWebCrawler.items import GenericwebcrawlerItem
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
            # see request result
            # print("THE URL: ", response.url)
            # print("RESPONSE: ")
            # print(response)
            # response("<em> <td> Halo, </td> aku text outlier </em>")
            title = response.xpath('//title//text()').extract()[0].strip()

            # select all texts between <p> tags except script tags: (double // to select all children too)
            bsoup = BeautifulSoup(response.text, 'html.parser')
            # remove <a> tags
            a_tags = bsoup.find_all('a')
            for a in a_tags:
                a.decompose()
            # remove <script> tags
            script_tags = bsoup.find_all('script')
            for s in script_tags:
                s.decompose()

            p_children = bsoup.find_all('p')
            # p_filtered = filter(self.tag_visible, p_children)
            # p_filtered =  u" ".join(t.strip() for t in p_filtered)
            # response = soup.xpath('//*[not(self::script) and not(self::a)]').extract()
            # p_children = response.xpath('//*[not(self::script) and not(self::a)]/p').extract()
            # print("P_CHILDREN: ", p_children)
            # temp = response.xpath('//*[not(self::script) and not(self::a)]/p/text()[re:test(., "\w+")]').extract()


            listOfSentences = []
            for child in p_children:
                child = child.get_text()
                string = child.strip()
                doc = self.nlp(string)
                # remove excess middle whitespaces & minimum 10 chars to be considered as a sentence
                sentences = [" ".join(sent.string.strip().split()) for sent in doc.sents if len(sent.string.strip()) > 10 ]
                listOfSentences.extend(sentences)

            all_urls = self.get_all_links(response)
            self.traversedLinks = self.traversedLinks|all_urls
            # accumulate result:
            results.append((title, response.meta['url'], listOfSentences, all_urls))

            if int(response.meta['depth']) < int(self.depth):
                for url in all_urls:
                    yield Request('%s' % url, callback=self.parse_req, meta={'url': url})
                if len(all_urls) > 0:
                    for url in all_urls:
                        yield dict(link=url, meta=dict(source=self.source, depth=response.meta['depth']))

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
