# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class GenericwebcrawlerItem(scrapy.Item):
    title = scrapy.Field()
    url = scrapy.Field()
    sentences = scrapy.Field()
    follow_links = scrapy.Field()


class KompaswebcrawlerItem(scrapy.Item):
    title = scrapy.Field()
    url = scrapy.Field()
    sentences = scrapy.Field()
    follow_links = scrapy.Field()

class CNNwebcrawlerItem(scrapy.Item):
    title = scrapy.Field()
    url = scrapy.Field()
    sentences = scrapy.Field()
    follow_links = scrapy.Field()