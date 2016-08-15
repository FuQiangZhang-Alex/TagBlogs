
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
        self.http = ul.PoolManager()

    def extract(self, xpath=''):
        res = self.http.request(method='GET', url=self.start_urls[0])
        xml_tree = etree.parse(source=BytesIO(res.data))
        entries = []
        for node in xml_tree.iter(tag='{http://www.sitemaps.org/schemas/sitemap/0.9}url'):
            children = node.getchildren()
            url = children[0].text
            cate_search = regex.search(pattern='(?<=/cate/).+(?=/)', string=url)
            cate = None
            if cate_search:
                cate = cate_search.captures()[0]
            else:
                cate = 'undefined'
            last_mod = children[1].text
            entry = {'url': url, 'cate': cate, 'lastmod': last_mod}
            page_number = self.get_pages(self, entry=entry)
            entry['page_number'] = page_number
            print(entry)
            entries.append(entry)
        return entries

    @staticmethod
    def get_pages(self, entry):
        """
        Get the largest page number of the given page
        :param self:
        :param entry: dict that contains page url and
        :return: the largest page number of the given page
        """
        if entry['cate'] == 'undefined':
            test_url = entry['url'] + 'default.html?page=2'
            test_page = self.http.request(method='GET', url=test_url)
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
                    return max(page_numbers)
                else:
                    page_number = 1
                    return page_number
        else:
            cate_url = entry['url']
            cate_page = self.http.request(method='GET', url=cate_url)
            html_parser = etree.HTMLParser()
            cate_page_tree = etree.parse(source=BytesIO(cate_page.data), parser=html_parser)
            cate_pages = cate_page_tree.xpath('//div[@id="paging_block"]/div[@class="pager"]/*')
            cate_page_numbers = list(map(lambda x: int(x),
                                         list(filter(lambda x: x is not None and x.isnumeric(),
                                                     list(map(lambda x: x.text, cate_pages))))))
            return max(cate_page_numbers)
