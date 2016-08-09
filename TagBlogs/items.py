# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy as sp


class TagblogsItem(sp.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class BlogEntry(sp.Item):
    url = sp.Field()  # blog's url, PK
    header = sp.Field()  # blog's header
    summary = sp.Field()  # summary of the blog
    author = sp.Field()  # author of the blog
    author_url = sp.Field()  # author's home page url, May be FK
    pub_time = sp.Field()
