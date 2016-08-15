
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

    def extract(self, xpath=''):
        http = ul.PoolManager()
        res = http.request(method='GET', url=self.start_urls[0])
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
                cate = ''
            last_mod = children[1].text
            entry = {'url': url, 'cate': cate, 'lastmod': last_mod}
            entries.append(entry)
        return entries

ss = SitemapSpider()
print(ss.extract())
