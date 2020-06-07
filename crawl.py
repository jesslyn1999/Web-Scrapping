from genericWebCrawler.genericWebCrawler.spiders.crawler import load_scraper


def start_scraping_job(
        root_url,
        keywords,  # keyword strings separated by ','
        allowed_domains=None,
        depth=0):
    allowed_domains = (",".join(allowed_domains)) if allowed_domains else ''
    load_scraper(root_url, keywords, allowed_domains, depth)


if __name__ == '__main__':
    start_scraping_job("https://www.bbc.com/indonesia/indonesia-52868562", keywords="warga,ternak", depth=0)
