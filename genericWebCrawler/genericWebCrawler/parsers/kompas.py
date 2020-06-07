from genericWebCrawler.genericWebCrawler.parsers.generic import GenericParser
from genericWebCrawler.genericWebCrawler.items import KompaswebcrawlerItem


class KompasParser(GenericParser):
    domain_name = '*kompas.com'

    def __init__(self):
        super().__init__()
        self._item = KompaswebcrawlerItem()
