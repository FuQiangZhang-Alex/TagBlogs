
from scrapy.spiders import SitemapSpider
from scrapy import Selector
import regex
from TagBlogs.items import SitemapEntry
from TagBlogs.items import BlogEntry


class CNBlogSitemapSpider(SitemapSpider):
    name = 'CNBlogSitemapSpider'
    sitemap_urls = ['http://www.cnblogs.com/sitemap.xml']
    sitemap_rules = [
        ('/cate/sharepoint/', 'parse_all')
    ]

    def __init__(self, *a, **kw):
        super(CNBlogSitemapSpider, self).__init__(*a, **kw)
        pass

    def parse(self, response):
        pass

    def parse_all(self, response):
        self.logger.info(response.url)
        # get sitemap entry info
        cate_search = regex.search(pattern='(?<=/cate/).+(?=/)', string=response.url)
        cate = None
        if cate_search:
            cate = cate_search.captures()[0]
        else:
            cate = ''
        self.logger.info(str(cate))
        sitemap_entry = SitemapEntry()
        sitemap_entry['url'] = response.url
        sitemap_entry['cate'] = cate

        # extract blog entries
        selector = Selector(response)
        post_list = selector.xpath('//div[@id="post_list"]/div[@class="post_item"]')
        for post_item in post_list:
            entry = BlogEntry()
            entry['url'] = post_item.xpath('div[@class="post_item_body"]/h3/a/@href').extract()
            entry['header'] = post_item.xpath('div[@class="post_item_body"]/h3/a/text()').extract()
            entry['summary'] = post_item.xpath('div[@class="post_item_body"]/p/text()').extract()
            entry['author_url'] = post_item.xpath('div[@class="post_item_body"]/div[@class="post_item_foot"]/a/@href')\
                .extract()
            entry['author'] = post_item.xpath('div[@class="post_item_body"]/div[@class="post_item_foot"]/a/text()')\
                .extract()
            entry['pub_time'] = post_item.xpath('div[@class="post_item_body"]/div[@class="post_item_foot"]/text()')\
                .extract()
            return sitemap_entry, entry
