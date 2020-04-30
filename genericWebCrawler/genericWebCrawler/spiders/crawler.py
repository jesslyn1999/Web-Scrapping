from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from .urlExtractor import create_crawler_class
from genericWebCrawler.genericWebCrawler import settings as local_settings


def loadScraper(_root, _allowed_domains, _depth):
    crawler_settings = Settings()
    crawler_settings.setmodule(local_settings)
    results, UrlExtractor = create_crawler_class()

    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(UrlExtractor, root=_root, allow_domains=_allowed_domains, depth=_depth)
    process.start() # the script will block here until the crawling is finished

    return results