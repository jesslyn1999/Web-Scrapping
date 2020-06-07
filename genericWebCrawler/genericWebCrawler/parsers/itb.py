from genericWebCrawler.genericWebCrawler.parsers.generic import GenericParser
from genericWebCrawler.genericWebCrawler.items import BbcwebcrawlerItem


class ItbParser(GenericParser):
    domain_name = '*itb.ac.id'

    def __init__(self):
        super().__init__()
        self._item = BbcwebcrawlerItem()
