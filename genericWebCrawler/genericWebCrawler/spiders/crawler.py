from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from .urlExtractor import create_crawler_class
from genericWebCrawler.genericWebCrawler import settings as local_settings
from genericWebCrawler.genericWebCrawler.parser import ParserHelper
from genericWebCrawler.genericWebCrawler import parsers
from db.db import crawl_result_collection, crawl_request_collection
from db.models import CrawlResult, CrawlRequest
import datetime
import google_scraper


parserHelper = None  # exported


def load_scraper(searchQuery, filterKeywords, _allowed_domains, _depth):
    global parserHelper
    parserHelper = ParserHelper(filterKeywords)
    parserHelper.register(
        [parsers.BbcParser(), parsers.ItbParser(), parsers.KompasParser(), parsers.KompasianaParser(),
         parsers.KompasTvParser(), parsers.KontanParser(), parsers.CNNParser(), parsers.GenericParser()])

    crawler_settings = Settings()
    crawler_settings.setmodule(local_settings)
    UrlExtractor, result = create_crawler_class()

    root_urls_list = google_scraper.get_google_search_results_link(searchQuery, filterKeywords, max_page=5)
    # root_urls_list = searchQuery

    crawl_request = CrawlRequest(searchQuery, filterKeywords, root_urls_list, datetime.datetime.utcnow(), None,
                                 "inProgress")
    insertion_request = crawl_request_collection.update_one({'SearchQuery': searchQuery}, {"$set": crawl_request.__dict__},
                                                        upsert=True)
    inserted_request_id = insertion_request.upserted_id

    if not inserted_request_id:
        inserted_request_id = crawl_request_collection.find_one({'SearchQuery': searchQuery})["_id"]

    process = CrawlerProcess(settings=crawler_settings)  # ALT: CrawlerProcess(get_project_settings())
    process.crawl(UrlExtractor, root=root_urls_list, allow_domains=_allowed_domains, depth=_depth)
    process.start()  # the script will block here until the crawling is finished

    # print("\n\nRESULT: \n", result)

    crawl_request.TimeFinish = datetime.datetime.utcnow()
    crawl_request.State = "finish"
    crawl_request_collection.update_one({'_id': inserted_request_id}, {"$set": crawl_request.__dict__})

    db_results = []
    for key in result:
        db_results.append({
            "URLPage": key,
            "News": result[key]
        })
    crawl_result = CrawlResult(inserted_request_id, db_results)
    insertion_result = crawl_result_collection.update({'Request': inserted_request_id}, crawl_result.__dict__, upsert=True)

    print("Inserted scraping result to DB")
    print(insertion_result)
