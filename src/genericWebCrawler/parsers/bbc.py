from src.genericWebCrawler.parsers.generic import GenericParser
from src.genericWebCrawler.items import BbcwebcrawlerItem


class BbcParser(GenericParser):
    domain_name = '*bbc.com'

    def __init__(self):
        super().__init__()
        self._item = BbcwebcrawlerItem()
