import scrapy as sp


class SpiderTest(sp.Spider):

    name = 'SpiderTest'
    start_urls = [
        'http://www.cnblogs.com/cate/beginner/2',
        'http://www.cnblogs.com/cate/life/1',
        'http://www.cnblogs.com/cate/life/2',
        'http://www.cnblogs.com/cate/life/3',
        'http://www.cnblogs.com/cate/life/200',
        'http://www.cnblogs.com/jack-zeng/default.html?page=2'
    ]

    def parse(self, response):
        self.logger.warning(response.url + ' ' + str(response.status))
