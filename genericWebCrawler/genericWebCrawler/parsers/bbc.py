from genericWebCrawler.genericWebCrawler.parsers.generic import GenericParser
from genericWebCrawler.genericWebCrawler.items import BbcwebcrawlerItem


class BbcParser(GenericParser):
    domain_name = '*bbc.com'

    def __init__(self):
        super().__init__()
        self._item = BbcwebcrawlerItem()
