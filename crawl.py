from genericWebCrawler.genericWebCrawler.spiders.crawler import load_scraper

google_search_api_key = "AIzaSyDBdC5Wx-nF_129NFfA87cDIB0TpJsdf7g"


def start_scraping_job(
        query,
        keywords,  # keyword strings separated by ','
        allowed_domains=None,
        depth=0):
    allowed_domains = (",".join(allowed_domains)) if allowed_domains else ''
    load_scraper(query, keywords, allowed_domains, depth)


if __name__ == '__main__':
    # start_scraping_job("https://www.bbc.com/indonesia/indonesia-52868562", keywords="warga,ternak", depth=0)
    start_scraping_job("pilkada kompas.com 2020", keywords="pilkada, kompas, 2020", depth=0)
    # start_scraping_job("https://www.google.com/search/about", keywords="", depth=0)
