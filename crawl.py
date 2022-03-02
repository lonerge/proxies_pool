# 2.获取模块(crawl和get组成):

import json
import time
import requests
from lxml import etree
from random import choice


class ProxyMetaclass(type):
    def __new__(cls, name, bases, attrs):
        count = 0
        attrs['__CrawlFunc__'] = []
        for k, v in attrs.items():
            if 'crawl_' in k:
                attrs['__CrawlFunc__'].append(k)
                count += 1
        attrs['__CrawlFuncCount__'] = count
        return type.__new__(cls, name, bases, attrs)

class Crawler(object, metaclass=ProxyMetaclass):

    headers = [{
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11'
    }, {
        'User-Agent': 'Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11'
    }, {
        'User-Agent': 'Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11'
    }]

    def get_proxies(self, callback):
        proxies = []
        for proxy in eval("self.{}()".format(callback)):
            print("获取代理成功", proxy)
            proxies.append(proxy)
        return proxies

    def crawl_kuaidaili(self, page_index=18):
        """

        :param page_index: 爬取的页数
        :return:ip:port形式的代理
        """
        start_url = 'https://www.kuaidaili.com/free/inha/{}/'
        urls = [start_url.format(page) for page in range(1, page_index+1)]
        for url in urls:
            time.sleep(1)
            print("Crawling:", url)
            res = requests.get(url, headers=choice(self.headers))
            html = etree.HTML(res.text)
            if res.status_code == 200:
                ip_list = html.xpath('//*[@id="list"]/table/tbody/tr')
                # print(ip_list)
                for one in ip_list:
                    # time.sleep(1)
                    ip = one.xpath('./td[1]/text()')[0]
                    port = one.xpath('./td[2]/text()')[0]
                    yield ':'.join([ip, port])
                    # print(':'.join([ip, port]))

    def crawl_beesproxy(self, page_index=18):
        start_url = 'https://www.beesproxy.com/free/page/{}'
        urls = [start_url.format(page) for page in range(1, page_index+1)]
        urls.append('https://www.beesproxy.com/free')
        for url in urls:
            time.sleep(1)
            print("Crawling:", url)
            res = requests.get(url, headers=choice(self.headers))
            html = etree.HTML(res.text)
            if res.status_code == 200:
                ip_list = html.xpath('//*[@id="article-copyright"]/figure/table/tbody/tr')
                # print(ip_list)
                for one in ip_list:
                    # time.sleep(1)
                    ip = one.xpath('./td[1]/text()')[0]
                    port = one.xpath('./td[2]/text()')[0]
                    yield ':'.join([ip, port])
                    # print(':'.join([ip, port]))






