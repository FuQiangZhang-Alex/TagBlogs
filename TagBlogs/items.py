# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Field
from scrapy import Item


class TagblogsItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class BlogEntry(Item):
    url = Field()  # blog's url, PK
    header = Field()  # blog's header
    cate = Field()
    summary = Field()  # summary of the blog
    author = Field()  # author of the blog
    author_url = Field()  # author's home page url, May be FK
    pub_time = Field()


class SitemapEntry(Item):
    url = Field()
    cate = Field()
    lastmod = Field()
