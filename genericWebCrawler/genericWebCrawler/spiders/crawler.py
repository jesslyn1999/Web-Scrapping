from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from .urlExtractor import create_crawler_class
from genericWebCrawler.genericWebCrawler import settings as local_settings
from genericWebCrawler.genericWebCrawler.parser import Parser
from genericWebCrawler.genericWebCrawler.parsers.generic import generic_parser
from genericWebCrawler.genericWebCrawler.parsers.kompas import kompas_parser
from genericWebCrawler.genericWebCrawler.parsers.itb import itb_ac_id_parser

parsers = None # exported

def loadScraper(_root, keywords, _allowed_domains, _depth):
    global parsers
    parsers = Parser(keywords)
    parsers.register('*itb.ac.id', itb_ac_id_parser)
    parsers.register('*kompas.com', kompas_parser)
    parsers.register('*', generic_parser)

    crawler_settings = Settings()
    crawler_settings.setmodule(local_settings)
    UrlExtractor = create_crawler_class()

    process = CrawlerProcess(settings=crawler_settings)  # ALT: CrawlerProcess(get_project_settings())
    process.crawl(UrlExtractor, root=_root, allow_domains=_allowed_domains, depth=_depth, letstryassume=_root)
    process.start()  # the script will block here until the crawling is finished