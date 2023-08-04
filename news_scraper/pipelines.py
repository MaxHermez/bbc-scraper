# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import pymongo
from itemadapter import ItemAdapter
from os import getenv


class MongoPipeline:
    collection_name = 'articles'

    def __init__(self):
        self._mongo_uri = getenv("MONGO_URI", None)
        self._mongo_db = getenv("MONGO_DB", "Scrapy_db")
        self._mongo_articles = getenv("MONGO_COL", "Articles")

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self._mongo_uri)
        self.db = self.client[self._mongo_db]
        self.articles_col = self.db[self._mongo_articles]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        self.articles_col.insert_one(dict(item))
        return item