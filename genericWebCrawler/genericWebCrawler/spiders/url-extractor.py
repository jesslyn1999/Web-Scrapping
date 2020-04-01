from scrapy.spiders import Spider
from scrapy import Request
from scrapy.linkextractors import LinkExtractor

import spacy
# from spacy.symbols import ORTH
from spacy.tokens import Token
Token.set_extension('tag', default=False)

def create_custom_tokenizer(nlp):
    from spacy import util
    from spacy.tokenizer import Tokenizer
    from spacy.lang.tokenizer_exceptions import TOKEN_MATCH
    prefixes =  nlp.Defaults.prefixes + ('^<i>',)
    suffixes =  nlp.Defaults.suffixes + ('</i>$',)
    # remove the tag symbols from prefixes and suffixes
    prefixes = list(prefixes)
    prefixes.remove('<')
    prefixes = tuple(prefixes)
    suffixes = list(suffixes)
    suffixes.remove('>')
    suffixes = tuple(suffixes)
    infixes = nlp.Defaults.infixes
    rules = nlp.Defaults.tokenizer_exceptions
    token_match = TOKEN_MATCH
    prefix_search = (util.compile_prefix_regex(prefixes).search)
    suffix_search = (util.compile_suffix_regex(suffixes).search)
    infix_finditer = (util.compile_infix_regex(infixes).finditer)
    return Tokenizer(nlp.vocab, rules=rules,
                     prefix_search=prefix_search,
                     suffix_search=suffix_search,
                     infix_finditer=infix_finditer,
                     token_match=token_match)


class UrlExtractor(Spider):
    name = 'url-extractor'
    start_urls = []
    index = 0
    nlp = spacy.load("en_core_web_sm", vectors=False, parser=False, entity=False)
    tokenizer = create_custom_tokenizer(nlp)
    nlp.tokenizer = tokenizer

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
        yield Request('%s' % self.source, callback=self.parse_req)

    def parse_req(self, response):
        # see request result
        print("THE URL: ", response.url)
        #print("THE CONTENT: ", response.text)
        with open("genericWebCrawler/out_htmls/"+ str(self.index) +".txt", 'w', encoding="utf-8") as out_html:
            self.index += 1
            doc = self.nlp(response.text)
            # for entry in doc:
            #     out_html.write(entry.text)
            out_html.write(str([entry.text for entry in doc]))



        all_urls = []
        if int(response.meta['depth']) <= int(self.depth):
            all_urls = self.get_all_links(response)
            for url in all_urls:
                yield Request('%s' % url, callback=self.parse_req)
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