from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from .urlExtractor import create_crawler_class
from genericWebCrawler.genericWebCrawler import settings as local_settings
from genericWebCrawler.genericWebCrawler.parser import parsers
from genericWebCrawler.genericWebCrawler.parsers.generic import generic_parser
from genericWebCrawler.genericWebCrawler.parsers.itb import itb_ac_id_parser

parsers.register('*itb.ac.id', itb_ac_id_parser)
parsers.register('*', generic_parser)

def loadScraper(_root, _allowed_domains, _depth):
    crawler_settings = Settings()
    crawler_settings.setmodule(local_settings)
    results, UrlExtractor = create_crawler_class()

    process = CrawlerProcess(settings=crawler_settings)  # ALT: CrawlerProcess(get_project_settings())
    process.crawl(UrlExtractor, root=_root, allow_domains=_allowed_domains, depth=_depth)
    process.start()  # the script will block here until the crawling is finished

    return results
