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
    start_scraping_job("https://www.cnnindonesia.com/nasional/20200607164937-20-510762/risma-usul-ke-khofifah-agar-tak-perpanjang-psbb-surabaya", keywords="warga,ternak", depth=0)
