# 3.测试模块
# aiohttp:异步请求库(用作测试性能优于requests库)
# 原因:requests库为同步请求库; 即发出一个请求后要等待网页加载完成后继续执行,如果目标服务器响应过慢,极其浪费时间


import aiohttp, asyncio
from db import RedisClient
import time


# 设置判断代理是否有效的响应码
VAILD_STATUS_CODES = [200]
# 测试地址,可以指定,也可以使用通用(baidu)
TEST_URL = 'HTTP://www.baidu.com'
# 单次最大的测试数量
MAX_TEST_SIZE = 10



class Test(object):
    def __init__(self):
        self.redis = RedisClient()

    async def test_single_proxy(self, proxy):
        """

        :param proxy: 单个代理
        :return: None
        """
        conn = aiohttp.TCPConnector(ssl=False)
        async with aiohttp.ClientSession(connector=conn) as session:
            try:
                # isinstance()判断某个对象是否为某类型
                if isinstance(proxy, bytes):
                    proxy = proxy.decode('utf-8')
                real_proxy = 'http://' + proxy
                print("正在测试.", proxy)
                async with session.get(TEST_URL, proxy=real_proxy, timeout=12)as response:
                    if response.status in VAILD_STATUS_CODES:
                        self.redis.max(proxy)
                        print("代理可用", proxy)
                    else:
                        self.redis.decrease(proxy)
                        print("响应码不合法", proxy)
            except (ConnectionRefusedError, TimeoutError, AttributeError):
                self.redis.decrease(proxy)
                print("代理请求失败..", proxy)

    def run(self):
        """
        测试主函数
        :return:
        """
        print("测试器运行中...")
        try:
            proxies = self.redis.all()
            loop = asyncio.get_event_loop()
            for i in range(0, len(proxies), MAX_TEST_SIZE):
                test_proxies = proxies[i: i+MAX_TEST_SIZE]
                tasks = [self.test_single_proxy(proxy) for proxy in test_proxies]
                loop.run_until_complete(asyncio.wait(tasks))
                time.sleep(3)
        except Exception as e:
            print("测试器发生错误..", e.args)


# test = Test()
# test.run()
