from genericWebCrawler.genericWebCrawler.spiders.crawler import loadScraper
from db.models import CrawlResult
from db.db import crawl_result_collection

def start_scraping_job(
    root_url,
    keywords, # keyword strings separated by ','
    allowed_domains=None,
    depth=0):
    allowed_domains = (",".join(allowed_domains)) if allowed_domains else ''
    loadScraper(root_url, keywords, allowed_domains, depth)


if __name__ == '__main__':
    start_scraping_job("https://regional.kompas.com/read/2020/05/31/07483571/ternak-warga-banyak-yang-hilang-misterius-ternyata-ini-penyebabnya", keywords="warga,ternak", depth=0)
