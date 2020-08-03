from src.genericWebCrawler.spiders.crawler import load_scraper, load_scraper_google


def start_scraping_job(
        google_query,
        keywords,  # filter keyword strings separated by ","
        # list of allowed domains, format {uri.scheme}://{uri.netloc}/,
        allowed_domains=None,
        # ex. ['https://www.koranmadura.com/', 'https://www.kompas.com/']
        depth=0):
    load_scraper(google_query, keywords, allowed_domains, depth)


# if __name__ == '__main__':
#    load_scraper(
#        "https://www.kompasiana.com/aremangadas/5ee6f582097f3656c42b2262/flamboyan-di-pinggir-hutan", filter_keywords="warga,ternak", depth=0)

# if __name__ == '__main__':
#     load_scraper("https://www.cnnindonesia.com/nasional/20200607164937-20-510762/risma-usul-ke-khofifah-agar-tak-perpanjang-psbb-surabaya", filter_keywords="warga,ternak", depth=0)

# if __name__ == "__main__":
#     load_scraper_google("pilkada kompas.com 2020", filter_keywords="pilkada, kompas, 2020", depth=0)

# if __name__ == "__main__":
#     load_scraper("https://nasional.kompas.com/read/2020/05/29/07092271/ini-alasan-pemerintah-tak-mau-tunda-pilkada-hingga-covid-19-berakhir?page=all", filter_keywords="pilkada, 2020", depth=0)

# if __name__ == "__main__":
#     load_scraper("https://finance.detik.com/berita-ekonomi-bisnis/d-5080751/deretan-nama-menteri-ekonomi-dalam-isu-liar-reshuffle/1", filter_keywords="pilkada, 2020", depth=0)

# if __name__ == "__main__":
#     load_scraper("https://bola.tempo.co/read/1361349/menang-telak-5-2-manchester-united-geser-chelsea-di-posisi-4/full&view=ok", filter_keywords="pilkada, 2020", depth=0)

# if __name__ == "__main__":
#     load_scraper("https://news.detik.com/berita/d-5081309/pengacara-pastikan-denny-siregar-akan-penuhi-pangilan-polisi?_ga=2.61665452.1458690852.1593938311-249100007.1584667622", filter_keywords="pilkada, 2020", depth=0)

# if __name__ == "__main__":
#     load_scraper("https://gaya.tempo.co/read/1361609/ramai-kalung-antivirus-corona-cek-harganya-di-pasaran", filter_keywords="corona", depth=0)

if __name__ == "__main__":
    load_scraper("https://news.detik.com/berita/d-5118071/paspor-djoko-tjandra-disoal-yasonna-sebut-penerbitannya-sudah-sesuai-uu?tag_from=news_mostpop", filter_keywords="pilkada, 2020", depth=0)
