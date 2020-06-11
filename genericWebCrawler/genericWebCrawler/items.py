# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
import json


class GenericwebcrawlerItem(scrapy.Item):
    URLNews = scrapy.Field()
    Title = scrapy.Field()
    Body = scrapy.Field()
    FollowLinks = scrapy.Field()

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, indent=4)


class KompaswebcrawlerItem(GenericwebcrawlerItem):
    Time = scrapy.Field()
    Source = scrapy.Field()
    Author = scrapy.Field()
    Editor = scrapy.Field()


class BbcwebcrawlerItem(GenericwebcrawlerItem):
    pass


class KompasianawebcrawlerItem(GenericwebcrawlerItem):
    CreatedTime = scrapy.Field()
    LastEdit = scrapy.Field()
    LastSeenNumber = scrapy.Field()
    LikeNumber = scrapy.Field()
    CommentNumber = scrapy.Field()


class KompasTvwebcrawlerItem(GenericwebcrawlerItem):
    Time = scrapy.Field()
    Editor = scrapy.Field()


class KontanwebcrawlerItem(GenericwebcrawlerItem):
    Time = scrapy.Field()
    Source = scrapy.Field()
    Editor = scrapy.Field()


class ItbwebcrawlerItem(GenericwebcrawlerItem):
    pass

