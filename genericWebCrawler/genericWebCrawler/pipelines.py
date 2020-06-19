import pymongo
from scrapy.exceptions import DropItem
from genericWebCrawler.genericWebCrawler import items


class GenericwebcrawlerPipeline:
    mongo_collection = 'generic'
    item_type = items.GenericwebcrawlerItem

    def __init__(self, mongo_uri, mongo_db):
        self._mongo_uri = mongo_uri
        self._mongo_db = mongo_db
        self._client = self._db = self._collection = None

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGODB_URI'),
            mongo_db=crawler.settings.get('MONGODB_DB', 'default_crawler_db'),
        )

    def open_spider(self, spider):
        self._client = pymongo.MongoClient(self._mongo_uri)
        self._db = self._client[self._mongo_db]
        self._collection = self._db[self.mongo_collection]

    def close_spider(self, spider):
        self._client.close()

    def process_item(self, item, spider):
        if not (type(item) is self.item_type and item["Body"]):
            return item
        for data in item:
            if not data:
                raise DropItem("Missing data!")
        self._collection.update({'URLNews': item['URLNews']}, dict(item), upsert=True)
        return item


class KompaswebcrawlerPipeline(GenericwebcrawlerPipeline):
    mongo_collection = 'kompas'
    item_type = items.KompaswebcrawlerItem


class CNNwebcrawlerPipeline(GenericwebcrawlerPipeline):
    mongo_collection = 'cnn'
    item_type = items.CNNwebcrawlerItem
    # @classmethod
    # def from_crawler(cls, crawler):
    #     return cls(
    #         mongo_uri=crawler.settings.get('MONGODB_URI'),
    #         mongo_db=crawler.settings.get('MONGODB_DB', 'default_items'),
    #         mongo_collection='cnn',
    #     )

    # def process_item(self, item, spider):
    #     if not isinstance(item, CNNwebcrawlerItem):
    #         return item
    #     for data in item:
    #         if not data:
    #             raise DropItem("Missing data!")
    #     self.collection.update({'url': item['url']}, dict(item), upsert=True)
    #     return item

class KompasTvwebcrawlerPipeline(GenericwebcrawlerPipeline):
    mongo_collection = 'kompas_tv'
    item_type = items.KompasTvwebcrawlerItem


class BbcwebcrawlerPipeline(GenericwebcrawlerPipeline):
    mongo_collection = 'bbc'
    item_type = items.BbcwebcrawlerItem


class ItbwebcrawlerPipeline(GenericwebcrawlerPipeline):
    mongo_collection = 'itb'
    item_type = items.ItbwebcrawlerItem


class KompasianawebcrawlerPipeline(GenericwebcrawlerPipeline):
    mongo_collection = 'kompasiana'
    item_type = items.KompasianawebcrawlerItem


class KontanwebcrawlerPipeline(GenericwebcrawlerPipeline):
    mongo_collection = 'kontan'
    item_type = items.KontanwebcrawlerItem
