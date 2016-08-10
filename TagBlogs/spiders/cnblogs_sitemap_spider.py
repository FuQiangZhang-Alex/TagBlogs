
from scrapy.spiders import XMLFeedSpider
from TagBlogs.items import SitemapEntry


class CNBlogSitemapSpider(XMLFeedSpider):
    name = 'CNBlogSitemapSpider'
    start_urls = ['http://www.cnblogs.com/sitemap.xml']
    namespaces = [('n', 'http://www.sitemaps.org/schemas/sitemap/0.9')]
    iterator = 'iternodes'  # This is actually unnecessary, since it's the default value
    itertag = 'n:url'

    def __init__(self):
        pass

    def parse_node(self, response, node):
        self.logger.info('parse node', node.extract())
        sitemap = SitemapEntry()
        sitemap['url'] = node.xpath('loc/text()').extract()
        return sitemap
