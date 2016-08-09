
import scrapy as sp
from TagBlogs.items import BlogEntry


class CNBlogsEntrySpider(sp.Spider):
    name = 'CNBlogsEntrySpider'
    start_urls = (
        'http://www.cnblogs.com/'
    )

    def __init__(self):
        pass

    def parse(self, response):
        selector = sp.Selector(response)
        post_list = selector.xpath('//div[@id="post_list"]/div[@class="post_item"]')
        for post_item in post_list:
            entry = BlogEntry()
            header = post_item.xpath('div[@class="post_item_body"]/h3/a/text()|'
                                     'div[@class="post_item_body"]/h3/a/@href|'
                                     'div[@class="post_item_body"]/p/text()|'
                                     'div[@class="post_item_body"]/div[@class="post_item_foot"]/text()|'
                                     'div[@class="post_item_body"]/div[@class="post_item_foot"]/a/text()|'
                                     'div[@class="post_item_body"]/div[@class="post_item_foot"]/a/@href').extract()
            entry['url'] = post_item.xpath('div[@class="post_item_body"]/h3/a/@href').extract()
            entry['header'] = post_item.xpath('div[@class="post_item_body"]/h3/a/text()').extract()
            entry['summary'] = post_item.xpath('div[@class="post_item_body"]/p/text()').extract()
            entry['author_url'] = post_item.xpath('div[@class="post_item_body"]/div[@class="post_item_foot"]/a/@href')\
                .extract()
            entry['author'] = post_item.xpath('div[@class="post_item_body"]/div[@class="post_item_foot"]/a/text()')\
                .extract()
            entry['pub_time'] = post_item.xpath('div[@class="post_item_body"]/div[@class="post_item_foot"]/text()')\
                .extract()
            return entry

