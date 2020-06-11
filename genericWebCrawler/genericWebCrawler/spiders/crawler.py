from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from .urlExtractor import create_crawler_class
from genericWebCrawler.genericWebCrawler import settings as local_settings
from genericWebCrawler.genericWebCrawler.parser import ParserHelper
from genericWebCrawler.genericWebCrawler import parsers
from db.db import crawl_result_collection
from db.models import CrawlResult
import google_scraper


parserHelper = None  # exported


def load_scraper(searchQuery, filterKeywords, _allowed_domains, _depth):
    global parserHelper
    parserHelper = ParserHelper(filterKeywords)
    parserHelper.register(
        [parsers.BbcParser(), parsers.ItbParser(), parsers.KompasParser(), parsers.KompasianaParser(),
         parsers.KompasTvParser(), parsers.KontanParser(), parsers.GenericParser()])

    crawler_settings = Settings()
    crawler_settings.setmodule(local_settings)
    UrlExtractor, result = create_crawler_class()

    root_urls_list = google_scraper.get_google_search_results_link(searchQuery, filterKeywords, max_page=5)
    # root_urls_list = "https://nasional.kontan.co.id/news/ada-wabah-corona-kpu-usul-tambahan-anggaran-pilkada-serentak"

    process = CrawlerProcess(settings=crawler_settings)  # ALT: CrawlerProcess(get_project_settings())
    process.crawl(UrlExtractor, root=root_urls_list, allow_domains=_allowed_domains, depth=_depth)
    process.start()  # the script will block here until the crawling is finished

    # print("\n\nRESULT: \n", result)

    db_results = []
    for key in result:
        db_results.append({
            "URLPage": key,
            "News": result[key]
        })
    crawl_result = CrawlResult(searchQuery, filterKeywords, db_results)
    insertion_result = crawl_result_collection.update({'SearchQuery': searchQuery}, crawl_result.__dict__, upsert=True)

    print("Inserted scraping result to DB")
    print(insertion_result)

