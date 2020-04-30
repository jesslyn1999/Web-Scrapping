# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
# from scrapy.conf import settings
# from scrapy.exceptions import DropItem
# from scrapy import log


class GenericwebcrawlerPipeline(object):
    def process_item(self, item, spider):
        return item


class MongoPipeline:

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    # def __init__(self):
        # connection = MongoClient(
        #     settings['MONGODB_SERVER'],
        #     settings['MONGODB_PORT'],
        #     connect=False  # connect db first instead running on background(default)
        # )
        # db = connection[settings['MONGODB_DB']]
        # self.collection = db[settings['MONGODB_COLLECTION']]
        # pass

    @classmethod
    def from_crawler(cls, crawler):
        print('HEYY IM HEREEE')
        print('=====================================================================')
        return cls(
            mongo_uri=crawler.settings.get('MONGODB_URI'),
            mongo_db=crawler.settings.get('MONGODB_DB', 'default_items')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        print('HEYY IM HEREEE')
        print(item)
        print('=====================================================================')
        print(spider)
        # for data in item:
        #     if not data:
        #         raise DropItem("Missing data!")
        # self.collection.update({'url': item['url']}, dict(item), upsert=True)
        # log.msg("Question added to MongoDB database!",
        #         level=log.DEBUG, spider=spider)
        return item
