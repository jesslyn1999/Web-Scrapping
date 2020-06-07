from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from .urlExtractor import create_crawler_class
from genericWebCrawler.genericWebCrawler import settings as local_settings
from genericWebCrawler.genericWebCrawler.parser import ParserHelper
from genericWebCrawler.genericWebCrawler import parsers

parserHelper = None  # exported


def load_scraper(_root, keywords, _allowed_domains, _depth):
    global parserHelper
    parserHelper = ParserHelper(keywords)
    parserHelper.register([parsers.BbcParser(), parsers.ItbParser(), parsers.KompasParser(), parsers.GenericParser()])

    crawler_settings = Settings()
    crawler_settings.setmodule(local_settings)
    UrlExtractor = create_crawler_class()

    process = CrawlerProcess(settings=crawler_settings)  # ALT: CrawlerProcess(get_project_settings())
    process.crawl(UrlExtractor, root=_root, allow_domains=_allowed_domains, depth=_depth)
    process.start()  # the script will block here until the crawling is finished
