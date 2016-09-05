
import scrapy as sp
from TagBlogs.items import BlogEntry
from Utils.cnblog_sitemap import SitemapSpider
import regex

# 'http://www.cnblogs.com/cate/life/#p189',
# 'http://www.cnblogs.com/njczy2010/default.html?page=11'


class CNBlogsEntrySpider(sp.Spider):
    name = 'CNBlogsEntrySpider'
    start_urls = []
    new_entries = {}

    def __init__(self):
        self.initialize()

    def initialize(self):
        ss = SitemapSpider()
        entries = ss.extract()
        self.new_entries = {}
        for entry in entries:
            url = entry['url']
            cate = entry['cate']
            pn = entry['page_number']
            if cate == '':
                for page_num in range(1, pn + 1):
                    self.start_urls.append(url + 'default.html?page=' + str(page_num))
            else:
                for page_num in range(1, pn + 1):
                    self.start_urls.append(url + str(page_num))
            self.new_entries[url] = entry
        self.logger.warning('( : CNBlogsEntrySpider initialized. : )')

    def parse(self, response):
        if response.status != 200:
            self.logger.error('Failed to open: ', response.url, 'error: ', response.status)
            return None
        entry_list = []
        selector = sp.Selector(response)
        entry_url = response.url
        # http://www.cnblogs.com/lsgsanxiao/default.html?page=4
        # http://www.cnblogs.com/cate/life/#p4
        cate_key = regex.search(pattern='http.+/', string=entry_url)
        cate = self.new_entries[cate_key.captures()[0]]['cate'] if cate_key else ''
        # use get xpath to get information from the response body
        post_list = selector.xpath('//div[@id="post_list"]/div[@class="post_item"]')
        if post_list:
            post_urls = post_list.xpath('div[@class="post_item_body"]/h3/a/@href').extract()
            post_headers = post_list.xpath('div[@class="post_item_body"]/h3/a/text()').extract()
            post_summaries = post_list.xpath('div[@class="post_item_body"]/p/text()').extract()
            post_pubs = post_list.xpath('div[@class="post_item_body"]/div[@class="post_item_foot"]/text()').extract()
            post_homes = post_list.xpath('div[@class="post_item_body"]/div[@class="post_item_foot"]/a/@href').extract()
            post_authors = post_list.xpath('div[@class="post_item_body"]/div[@class="post_item_foot"]/a/text()')\
                .extract()
            post_pubs = list(filter(lambda x: not regex.search(pattern='                    \r\n    ', string=x)
                                    , post_pubs))
            pages = len(set(post_urls))
            if pages == len(post_headers) == len(post_summaries) == len(post_pubs) \
                    == len(post_homes) == len(post_authors):
                for i in range(0, len(post_urls)):
                    post_header = post_headers[i]
                    post_url = post_urls[i]
                    post_summary = post_summaries[i]
                    post_pub = post_pubs[i]
                    post_home_search = regex.search(pattern='http://www\.cnblogs\.com/.+/(?=p)', string=post_url[0])
                    post_home = post_home_search.captures()[0] if post_home_search else ''
                    author_search = regex.search(pattern='(?<=http://www\.cnblogs\.com/).+(?=/p)', string=post_url)
                    post_author = author_search.captures()[0] if post_home_search else ''
                    entry = BlogEntry()
                    entry['url'] = post_url
                    entry['header'] = post_header
                    entry['summary'] = post_summary
                    entry['author_url'] = post_home
                    entry['author'] = post_author
                    pub_time_search = regex.search(pattern='\d{4}-\d{2}-\d{2} \d{2}:\d{2}', string=post_pub)
                    entry['pub_time'] = pub_time_search.captures()[0] if pub_time_search else ''
                    entry['cate'] = cate
                    entry['source'] = entry_url
                    entry_list.append(entry)
            else:
                self.logger.error('length mismatch.')
                self.logger.error(post_urls)

        else:
            post_headers = selector.xpath('//div[@class="day"]/div[@class="postTitle"]/a/text()').extract()
            post_urls = selector.xpath('//div[@class="day"]/div[@class="postTitle"]/a/@href').extract()
            post_summaries = selector.xpath('//div[@class="day"]/div[@class="c_b_p_desc"]/text()').extract()
            post_pubs = selector.xpath('//div[@class="day"]/div[@class="postDesc"]/text()').extract()
            pages = len(set(post_urls))
            if pages == len(post_headers) == len(post_pubs) == len(post_summaries):
                for i in range(0, len(post_urls)):
                    post_header = post_headers[i]
                    post_url = post_urls[i]
                    post_summary = post_summaries[i]
                    post_pub = post_pubs[i]
                    post_home_search = regex.search(pattern='http://www\.cnblogs\.com/.+/(?=p)', string=post_url)
                    post_home = post_home_search.captures()[0] if post_home_search else ''
                    author_search = regex.search(pattern='(?<=http://www\.cnblogs\.com/).+(?=/p)', string=post_url)
                    post_author = author_search.captures()[0] if post_home_search else ''
                    entry = BlogEntry()
                    entry['url'] = post_url
                    entry['header'] = post_header
                    entry['summary'] = post_summary
                    entry['author_url'] = post_home
                    entry['author'] = post_author
                    pub_time_search = regex.search(pattern='\d{4}-\d{2}-\d{2} \d{2}:\d{2}', string=post_pub)
                    entry['pub_time'] = pub_time_search.captures()[0] if pub_time_search else ''
                    entry['cate'] = cate
                    entry['source'] = entry_url
                    entry_list.append(entry)
            else:
                self.logger.error('length mismatch.')
                self.logger.error(post_urls)
        return entry_list
