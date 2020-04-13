from scrapy.crawler import CrawlerProcess
from .urlExtractor import create_crawler_class

def loadScraper(_root, _allowed_domains, _depth):
    results, UrlExtractor = create_crawler_class()

    process = CrawlerProcess({})
    process.crawl(UrlExtractor, root=_root, allow_domains=_allowed_domains, depth=_depth)
    process.start() # the script will block here until the crawling is finished

    return results