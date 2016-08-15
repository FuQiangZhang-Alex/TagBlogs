
from scrapy import Spider


class TestSpider(Spider):
    name = 'TestSpider'
    start_urls = (
        'http://www.cnblogs.com/',
    )

    def __init__(self):
        pass

    def parse(self, response):
        self.logger.info('TestSpider')
        return {'a': 2, 'b': 3, 'c': 4}
