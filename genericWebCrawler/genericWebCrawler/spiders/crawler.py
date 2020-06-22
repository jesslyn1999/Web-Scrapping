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


def init_crawl_request(search_query, filter_keywords, root_urls_list):
    crawl_request = CrawlRequest(search_query, filter_keywords, root_urls_list, datetime.datetime.utcnow(), None, "inProgress")
    insertion_request = crawl_request_collection.update_one({'SearchQuery': search_query},
                                                            {"$set": crawl_request.__dict__},
                                                            upsert=True)
    inserted_request_id = insertion_request.upserted_id

    if not inserted_request_id:
        inserted_request_id = crawl_request_collection.find_one({'SearchQuery': search_query})["_id"]

    return crawl_request, inserted_request_id


def finish_crawl_request(crawl_request, request_id, result):
    crawl_request.TimeFinish = datetime.datetime.utcnow()
    crawl_request.State = "finish"
    crawl_request_collection.update_one({'_id': request_id}, {"$set": crawl_request.__dict__})

    db_results = []
    for key in result:
        db_results.append({
            "URLPage": key,
            "News": result[key]
        })
    crawl_result = CrawlResult(request_id, db_results)
    insertion_result = crawl_result_collection.update({'Request': request_id}, crawl_result.__dict__, upsert=True)
    return insertion_result


def begin_crawl(root_urls, filter_keywords, allowed_domains, depth):
    print("[*] Begin crawling", len(root_urls), "url(s)")
    global parserHelper
    parserHelper = ParserHelper(filter_keywords)
    parserHelper.register(
        [parsers.BbcParser(), parsers.ItbParser(), parsers.KompasParser(), parsers.KompasianaParser(),
         parsers.KompasTvParser(), parsers.KontanParser(), parsers.CNNParser(), parsers.GenericParser()])

    crawler_settings = Settings()
    crawler_settings.setmodule(local_settings)
    UrlExtractor, result = create_crawler_class()

    process = CrawlerProcess(settings=crawler_settings)  # ALT: CrawlerProcess(get_project_settings())
    process.crawl(UrlExtractor, root=root_urls, allow_domains=allowed_domains, depth=depth)
    process.start()  # the script will block here until the crawling is finished

    print("[x] Finished crawling")
    return result


def load_scraper_google(search_query, filter_keywords=None, allowed_domains=None, depth=0, max_page=5):
    print("[*] Acquiring links from Google")
    root_urls_list = google_scraper.get_google_search_results_link(search_query, filter_keywords, max_page)

    crawl_request, request_id = init_crawl_request(search_query, filter_keywords, root_urls_list)
    result = begin_crawl(root_urls_list, filter_keywords, allowed_domains, depth)
    insertion_result = finish_crawl_request(crawl_request, request_id, result)

    print("[x] Inserted Google scraping result", insertion_result)
    return result


def load_scraper(root_urls, filter_keywords=None, allowed_domains=None, depth=0):
    crawl_request, request_id = init_crawl_request(None, filter_keywords, root_urls)
    result = begin_crawl(root_urls, filter_keywords, allowed_domains, depth)
    insertion_result = finish_crawl_request(crawl_request, request_id, result)

    print("[x] Inserted URL scraping result", insertion_result)
    return result