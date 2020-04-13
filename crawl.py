from genericWebCrawler.genericWebCrawler.spiders.crawler import loadScraper
from db.models import CrawlResult
from db.db import crawl_result_collection

def start_scraping_job(root_url, allowed_domains=None, depth=1):
    allowed_domains = (",".join(allowed_domains)) if allowed_domains else '*'
    results = loadScraper(root_url, allowed_domains, depth)

    crawl_results = []
    for result in results:
        title, url, sentences = result
        crawl_result = CrawlResult(title=title, url=url, sentences=sentences)
        crawl_results.append(crawl_result.__dict__)

    insertion_result = crawl_result_collection.insert_many(crawl_results)

    print("Inserted scraping result to DB")
    print(insertion_result)


if (__name__ == '__main__'):
    start_scraping_job("https://www.itb.ac.id")
