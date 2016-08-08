
import scrapy as sc


class CNBlogsEntrySpider(sc.Spider):
    name = 'CNBlogsEntrySpider'
    start_urls = (
        'http://www.cnblogs.com/'
    )

    def __init__(self):
        pass

    def parse(self, response):
        selector = sc.Selector(response)
        entries = selector.xpath('//div[@id="post_list"]')
        return entries

