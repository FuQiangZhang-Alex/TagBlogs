# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json


class TagblogsPipeline(object):

    def __init__(self):
        self.file = open(file='blog_entry.json', mode='w')

    def process_item(self, item, spider):
        print('TagblogsPipeline #2')
        line = json.dumps(dict(item)) + '\n'
        self.file.write(line)
        return item


class SitemapPipeline(object):

    def __init__(self):
        pass

    def process_item(self, item, spider):
        print('SitemapPipeline #1')
        return item
