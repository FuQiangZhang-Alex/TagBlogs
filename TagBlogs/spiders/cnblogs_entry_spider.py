
import scrapy as sp
from TagBlogs.items import BlogEntry
from Utils.cnblog_sitemap import SitemapSpider
import regex


class CNBlogsEntrySpider(sp.Spider):
    name = 'CNBlogsEntrySpider'
    start_urls = [
        'http://www.cnblogs.com/cate/life/#p189',
        'http://www.cnblogs.com/njczy2010/default.html?page=11'
    ]
    new_entries = {}

    # def __init__(self):
    #     ss = SitemapSpider()
    #     entries = ss.extract()
    #     self.new_entries = {}
    #     for entry in entries:
    #         url = entry['url']
    #         cate = entry['cate']
    #         pn = entry['page_number']
    #         self.start_urls.append(url)
    #         if cate == 'undefined':
    #             for page_num in range(2, pn + 1):
    #                 self.start_urls.append(url + 'default.html?page=' + str(page_num))
    #         else:
    #             for page_num in range(2, pn + 1):
    #                 self.start_urls.append(url + '#p' + str(page_num))
    #         f = open(file='a.txt', mode='w')
    #         f.write(str(self.start_urls))
    #         self.new_entries[url] = entry

    def parse(self, response):
        self.logger.info('parse')
        selector = sp.Selector(response)
        entry = BlogEntry()
        entry_url = response.url
        key_search = regex.search(pattern='^http://www\.cnblogs\.com/.+/', string=entry_url)
        cate = ''
        entry['cate'] = cate
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
            if len(post_urls) == len(post_headers) == len(post_summaries) == len(post_pubs) \
                    == len(post_homes) == len(post_authors):
                print(len(post_authors), post_authors)

        else:
            post_headers = selector.xpath('//div[@class="day"]/div[@class="postTitle"]/a/text()').extract()
            post_urls = selector.xpath('//div[@class="day"]/div[@class="postTitle"]/a/@href').extract()
            post_summaries = selector.xpath('//div[@class="day"]/div[@class="c_b_p_desc"]/text()').extract()
            post_pubs = selector.xpath('//div[@class="day"]/div[@class="postDesc"]/text()').extract()
            if len(post_headers) == len(post_urls) == len(post_pubs) == len(post_summaries):
                for i in range(0, len(post_urls)):
                    post_header = post_headers[i]
                    post_url = post_urls[i]
                    post_summary = post_summaries[i]
                    post_pub = post_pubs[i]
                    post_home_search = regex.search(pattern='http://www\.cnblogs\.com/.+/(?=p)', string=post_url[0])
                    post_home = post_home_search.captures()[0] if post_home_search else ''
                    post_author = ''
                    entry['url'] = post_url
                    entry['header'] = post_header
                    entry['summary'] = post_summary
                    entry['author_url'] = post_home
                    entry['author'] = post_author
                    entry['pub_time'] = post_pub
                    entry['cate'] = cate

    def parse_bk(self, response):
        selector = sp.Selector(response)
        post_list = selector.xpath('//div[@id="post_list"]/div[@class="post_item"]')
        entry_url = response.url
        key_search = regex.search(pattern='^http://www\.cnblogs\.com/.+/', string=entry_url)
        cate = ''
        if key_search:
            key = key_search.captures()[0]
            cate = self.new_entries[key]['cate']
        else:
            cate = 'undefined'
        for post_item in post_list:
            entry = BlogEntry()
            post_url = post_item.xpath('div[@class="post_item_body"]/h3/a/@href').extract()
            post_header = post_item.xpath('div[@class="post_item_body"]/h3/a/text()').extract()
            post_summary = post_item.xpath('div[@class="post_item_body"]/p/text()').extract()
            post_home = post_item.xpath('div[@class="post_item_body"]/div[@class="post_item_foot"]/a/@href').extract()
            post_author = post_item.xpath('div[@class="post_item_body"]/div[@class="post_item_foot"]/a/text()').extract()
            post_pub = post_item.xpath('div[@class="post_item_body"]/div[@class="post_item_foot"]/text()').extract()
            entry['url'] = post_url[0] if post_url else ''
            entry['header'] = post_header[0] if post_header else ''
            entry['summary'] = post_summary[0] if post_summary else ''
            entry['author_url'] = post_home[0] if post_home else ''
            entry['author'] = post_author[0] if post_author else ''
            entry['pub_time'] = post_pub[0] if post_pub else ''
            entry['cate'] = cate
            return entry
