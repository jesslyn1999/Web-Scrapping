# -*- coding: utf-8 -*-

# Scrapy settings for genericWebCrawler project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html
from db.db import mongodb_db, mongodb_uri

BOT_NAME = 'genericWebCrawler'

SPIDER_MODULES = ['genericWebCrawler.genericWebCrawler.spiders']
NEWSPIDER_MODULE = 'genericWebCrawler.genericWebCrawler.spiders'
ITEM_PIPELINES = {
    'genericWebCrawler.genericWebCrawler.pipelines.GenericwebcrawlerPipeline': 300,
    'genericWebCrawler.genericWebCrawler.pipelines.KompaswebcrawlerPipeline': 300,
    'genericWebCrawler.genericWebCrawler.pipelines.CNNwebcrawlerPipeline': 300,
    'genericWebCrawler.genericWebCrawler.pipelines.BbcwebcrawlerPipeline': 300,
    'genericWebCrawler.genericWebCrawler.pipelines.ItbwebcrawlerPipeline': 300,
    'genericWebCrawler.genericWebCrawler.pipelines.KompasianawebcrawlerPipeline': 300,
    'genericWebCrawler.genericWebCrawler.pipelines.KompasTvwebcrawlerPipeline': 300,
    'genericWebCrawler.genericWebCrawler.pipelines.KontanwebcrawlerPipeline': 300,
}
LOG_LEVEL = 'ERROR'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'genericWebCrawler (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

MONGODB_URI = mongodb_uri
MONGODB_DB = mongodb_db

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'genericWebCrawler.middlewares.GenericwebcrawlerSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'genericWebCrawler.middlewares.GenericwebcrawlerDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
#ITEM_PIPELINES = {
#    'genericWebCrawler.pipelines.GenericwebcrawlerPipeline': 300,
#}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
