from genericWebCrawler.genericWebCrawler.spiders.crawler import loadScraper
from db.models import CrawlResult
from db.db import crawl_result_collection

def start_scraping_job(root_url, allowed_domains=None, depth=0):
    allowed_domains = (",".join(allowed_domains)) if allowed_domains else ''
    loadScraper(root_url, allowed_domains, depth)


if __name__ == '__main__':
    start_scraping_job("https://www.ui.ac.id", depth=0)
