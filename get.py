# 2.获取模块(crawl和get组成):
# 动态的调用crawl里面的方法,抓取代理存入数据库


from db import RedisClient
from crawl import Crawler
import time


POOL_UPPER_THRESHOLD = 1000

class Getter(object):
    def __init__(self):
        self.redis = RedisClient()
        self.crawler = Crawler()

    # def is_over_threshold(self):
    #     if self.redis.count() >= POOL_UPPER_THRESHOLD:
    #         return True
    #     else:
    #         return False

    def run(self):
        print("获取器开始执行...")
        if self.redis.count() < POOL_UPPER_THRESHOLD:
            # print("1..")
            for callback_label in range(self.crawler.__CrawlFuncCount__):
                print("crawling..")
                # time.sleep(2)
                callback = self.crawler.__CrawlFunc__[callback_label]
                proxies = self.crawler.get_proxies(callback)
                for proxy in proxies:
                    print("saving..", proxy)
                    # time.sleep(1)
                    self.redis.add(proxy)



# getter = Getter()
# getter.run()