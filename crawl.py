from genericWebCrawler.genericWebCrawler.spiders.crawler import load_scraper


def start_scraping_job(
        google_query,
        keywords,  # filter keyword strings separated by ","
        # list of allowed domains, format {uri.scheme}://{uri.netloc}/,
        allowed_domains=None,
        # ex. ['https://www.koranmadura.com/', 'https://www.kompas.com/']
        depth=0):
    load_scraper(google_query, keywords, allowed_domains, depth)


# if __name__ == '__main__':
#    start_scraping_job(
#        "https://www.kompasiana.com/aremangadas/5ee6f582097f3656c42b2262/flamboyan-di-pinggir-hutan", keywords="warga,ternak", depth=0)

# if __name__ == '__main__':
#     start_scraping_job("https://www.cnnindonesia.com/nasional/20200607164937-20-510762/risma-usul-ke-khofifah-agar-tak-perpanjang-psbb-surabaya", keywords="warga,ternak", depth=0)

if __name__ == "__main__":
    start_scraping_job("pilkada kompas.com 2020", keywords="pilkada, kompas, 2020", depth=0)

# if __name__ == "__main__":
#     start_scraping_job("https://nasional.kompas.com/read/2020/05/29/07092271/ini-alasan-pemerintah-tak-mau-tunda-pilkada-hingga-covid-19-berakhir?page=all", keywords="pilkada, kompas, 2020", depth=0)
