from src.genericWebCrawler.parsers.generic import GenericParser
from src.genericWebCrawler.items import ItbwebcrawlerItem


class ItbParser(GenericParser):
    domain_name = '*itb.ac.id'

    def __init__(self):
        super().__init__()
        self._item = ItbwebcrawlerItem()
