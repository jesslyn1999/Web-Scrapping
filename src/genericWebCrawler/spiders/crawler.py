import scrapy.crawler as crawler
from scrapy.settings import Settings
from .urlExtractor import create_crawler_class
from bson import ObjectId
import datetime
from multiprocessing import Process, Queue
from twisted.internet import reactor
from db.db import crawl_request_collection
from db.models import CrawlRequest
from src.genericWebCrawler import settings as local_settings
from src.genericWebCrawler.parser import ParserHelper
from src.genericWebCrawler import parsers
from src.selenium import google_scraper

parserHelper = None  # exported


def init_crawl_request(search_query, filter_keywords, root_urls_list):
    crawl_request = CrawlRequest(search_query, filter_keywords, root_urls_list, datetime.datetime.utcnow(), None, "inProgress")
    insertion_request = crawl_request_collection.update_one({'SearchQuery': search_query},
                                                            {"$set": crawl_request.__dict__},
                                                            upsert=True)
    inserted_request_id = insertion_request.upserted_id

    if not inserted_request_id:
        inserted_request_id = crawl_request_collection.find_one({'SearchQuery': search_query})["_id"]

    return crawl_request, str(inserted_request_id)


def finish_crawl_request(crawl_request, request_id):
    crawl_request.TimeFinish = datetime.datetime.utcnow()
    crawl_request.State = "finish"
    insertion_result = crawl_request_collection.update_one(
        {'_id': ObjectId(request_id)}, {"$set": crawl_request.__dict__}
    )
    return insertion_result.raw_result


UrlExtractor, result = create_crawler_class()

# function helper for run_spider
def run_reactor(crawler_settings, result_queue, spider, root_urls, allowed_domains, depth, request_id):
    try:
        runner = crawler.CrawlerRunner(settings=crawler_settings)
        deferred = runner.crawl(spider, root=root_urls, allow_domains=allowed_domains, depth=depth,
                                request_id=request_id)
        deferred.addBoth(lambda _: reactor.stop())
        reactor.run()
        result_queue.put(None)
    except Exception as e:
        result_queue.put(e)

# the wrapper to make it run more times
def run_spider(spider, crawler_settings, root_urls, allowed_domains, depth, request_id):
    q = Queue()
    p = Process(target=run_reactor, args=(crawler_settings, q, spider, root_urls, allowed_domains, depth,
                                request_id,))
    p.start()
    result_spider = q.get()
    p.join()

    if result_spider is not None:
        raise result_spider

def begin_crawl(request_id, root_urls, filter_keywords, allowed_domains, depth, stop_after_crawl=True):
    print("[*] Begin crawling", len(root_urls), "url(s)")
    global parserHelper
    parserHelper = ParserHelper(filter_keywords)
    parserHelper.register(
        [parsers.BbcParser(), parsers.ItbParser(), parsers.KompasParser(), parsers.KompasianaParser(),
         parsers.KompasTvParser(), parsers.KontanParser(), parsers.CNNParser(), parsers.TempoParser(),
         parsers.DetikParser(), parsers.GenericParser()])

    crawler_settings = Settings()
    crawler_settings.setmodule(local_settings)

    run_spider(spider=UrlExtractor, crawler_settings=crawler_settings, root_urls=root_urls, allowed_domains=allowed_domains, depth=depth, request_id=request_id)

    print("[x] Finished crawling")
    return result

def get_links_from_keyword(search_query, filter_keywords="", max_page=5):
    print("[*] Acquiring links from Google")
    root_urls_list = google_scraper.get_google_search_results_link(search_query, filter_keywords, max_page)
    return root_urls_list

def load_scraper_google(search_query, filter_keywords=None, allowed_domains=None, depth=0, max_page=5):
    root_urls_list = get_links_from_keyword(search_query, filter_keywords, max_page)
    crawl_request, request_id = init_crawl_request(search_query, filter_keywords, root_urls_list)
    result = begin_crawl(request_id, root_urls_list, filter_keywords, allowed_domains, depth)
    insertion_result = finish_crawl_request(crawl_request, request_id)

    print("[x] Inserted Google scraping result", insertion_result)
    return result


def load_scraper(root_urls, filter_keywords=None, allowed_domains=None, depth=0):
    crawl_request, request_id = init_crawl_request(None, filter_keywords, root_urls)
    result = begin_crawl(request_id, root_urls, filter_keywords, allowed_domains, depth)
    insertion_result = finish_crawl_request(crawl_request, request_id)

    print("[x] Inserted URL scraping result", insertion_result)
    return result
