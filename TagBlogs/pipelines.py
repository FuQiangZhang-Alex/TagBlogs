# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
from pymongo import MongoClient
from scrapy.exceptions import DropItem


class TagblogsPipeSave2Mongo(object):

    collection_name = 'BlogEntry'

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.client = None
        self.db = None
        self.file = open(file='blog_entry.json', mode='w')

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'TagBlogs')
        )

    def open_spider(self, spider):
        self.client = MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + '\n'
        # check if the item already exists
        # exists = list(self.db[self.collection_name].find(filter={'url': item['url']}, limit=1))
        self.db[self.collection_name].insert(dict(item))
        self.file.write(line)
        return item


class TagblogsFilterNoneItem(object):

    def process_item(self, item, spider):
        if item is None:
            raise DropItem()
        else:
            return item
