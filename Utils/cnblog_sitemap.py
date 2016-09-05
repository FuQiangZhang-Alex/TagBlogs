
import urllib3 as ul
from lxml import etree
from io import BytesIO
import regex


class SitemapSpider:
    start_urls = [
        'http://www.cnblogs.com/sitemap.xml'
    ]

    def __init__(self, itertag='url'):
        self.itertag = itertag
        self.http = ul.PoolManager(num_pools=100)

    def extract(self, xpath=''):
        print('SitemapSpider')
        res = self.http.request(method='GET', url=self.start_urls[0])
        xml_tree = etree.parse(source=BytesIO(res.data))
        entries = []
        url_nodes = list(xml_tree.iter(tag='{http://www.sitemaps.org/schemas/sitemap/0.9}url'))
        print(type(url_nodes))
        for node in url_nodes:
            children = node.getchildren()  # subnodes under url node
            url = children[0].text
            cate_search = regex.search(pattern='(?<=http://www\.cnblogs\.com/cate/).+(?=/)', string=url)
            cate = cate_search.captures()[0] if cate_search else ''
            last_mod = children[1].text
            entry = {'url': url, 'cate': cate, 'lastmod': last_mod}
            page_number = self.get_pages(self, entry=entry)
            if page_number > 0:
                entry['page_number'] = page_number
                entries.append(entry)
            else:
                continue
        return entries

    @staticmethod
    def get_pages(self, entry):
        """
        Get the largest page number of the given page
        :param self:
        :param entry: dict that contains page url and
        :return: the largest page number of the given page
        """
        if entry['cate'] == '':
            test_url = entry['url'] + 'default.html?page=2'
            test_page = self.http.request(method='GET', url=test_url)
            response_code = test_page.status
            if response_code != 200:
                print(test_url)
                return 0
            parser = etree.HTMLParser()
            test_page_tree = etree.parse(source=BytesIO(test_page.data), parser=parser)
            pages = test_page_tree.xpath('//div[@id="homepage_top_pager"]/div[@class="pager"]')
            strange_pages = test_page_tree.xpath('//div[@id="pager"]/*')
            if pages:
                page_number = int(str(regex.search(pattern='\d+', string=pages[0].text).captures()[0]))
                return page_number
            else:
                if strange_pages:
                    page_numbers = list(map(lambda x: int(x),
                                            list(filter(lambda x: x is not None and x.isnumeric(),
                                                        list(map(lambda x: x.text, strange_pages))))))
                    if page_numbers:
                        return max(page_numbers)
                    else:
                        return 1
                else:
                    return 1
        else:
            cate_url = entry['url']
            cate_page = self.http.request(method='GET', url=cate_url)
            cate_response_code = cate_page.status
            if cate_response_code != 200:
                print(cate_url)
                return 0
            html_parser = etree.HTMLParser()
            cate_page_tree = etree.parse(source=BytesIO(cate_page.data), parser=html_parser)
            cate_pages = cate_page_tree.xpath('//div[@id="paging_block"]/div[@class="pager"]/*')
            cate_page_numbers = list(map(lambda x: int(x),
                                         list(filter(lambda x: x is not None and x.isnumeric(),
                                                     list(map(lambda x: x.text, cate_pages))))))
            if cate_page_numbers:
                return max(cate_page_numbers)
            else:
                return 1
