# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
import json
# from scrapy.conf import settings
# from scrapy import log
from scrapy.exceptions import DropItem
from genericWebCrawler.genericWebCrawler.items import GenericwebcrawlerItem
from genericWebCrawler.genericWebCrawler.items import KompaswebcrawlerItem
from genericWebCrawler.genericWebCrawler.items import CNNwebcrawlerItem

class WebcrawlerPipeline:
    def __init__(self, mongo_uri, mongo_db, mongo_collection):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.mongo_collection = mongo_collection
        self.client = self.db = self.collection = None

    @classmethod
    def from_crawler(cls, crawler):
        raise NotImplementedError

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
        self.collection = self.db[self.mongo_collection]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        raise NotImplementedError


class GenericwebcrawlerPipeline(WebcrawlerPipeline):
    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGODB_URI'),
            mongo_db=crawler.settings.get('MONGODB_DB', 'default_items'),
            mongo_collection='generic_web',
        )

    def process_item(self, item, spider):
        if not isinstance(item, GenericwebcrawlerItem):
            return item
        for data in item:
            if not data:
                raise DropItem("Missing data!")
        self.collection.update({'url': item['url']}, dict(item), upsert=True)
        return item


class KompaswebcrawlerPipeline(WebcrawlerPipeline):
    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGODB_URI'),
            mongo_db=crawler.settings.get('MONGODB_DB', 'default_items'),
            mongo_collection='kompas',
        )

    def process_item(self, item, spider):
        if not isinstance(item, KompaswebcrawlerItem):
            return item
        for data in item:
            if not data:
                raise DropItem("Missing data!")
        self.collection.update({'url': item['url']}, dict(item), upsert=True)
        return item


class CNNwebcrawlerPipeline(WebcrawlerPipeline):
    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGODB_URI'),
            mongo_db=crawler.settings.get('MONGODB_DB', 'default_items'),
            mongo_collection='cnn',
        )

    def process_item(self, item, spider):
        if not isinstance(item, CNNwebcrawlerItem):
            return item
        for data in item:
            if not data:
                raise DropItem("Missing data!")
        self.collection.update({'url': item['url']}, dict(item), upsert=True)
        return item