# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from cnblogs.spiders.url_spider import UrlSpider
import json


class CnblogsPipeline(object):

    def __init__(self):
        self.file = open(file='blog_entry.json', mode='w')

    def process_item(self, item, spider):
        print(item['header'])
        line = json.dumps(dict(item)) + '\n'
        self.file.write(line)
        return item
