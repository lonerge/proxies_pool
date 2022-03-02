# 维护代理池:
#     1.存储模块
#         一般使用存储的方式:Redis的有序集合(实现存储代理,且保证代理不重复)
#
#     2.获取模块
#         从各大代理网站抓取代理; 代理形式为: ip+端口; 抓取成功存入数据库
#
#     3.检测模块
#         定时检测数据库中的代理(爬取哪个网站就检测哪个网站,不然就测试百度);
#         标识每一个代理的状态,100分可用,每一次检测,对不可用的代理-1分,分数低于一定阈值则删除该代理
#
#     4.接口模块
#         需要用API来提供对外服务的接口(设计一个WebAPI接口,随机返回一个可用的代理)



# 1.存储模块:

import redis
import random


MAX_SCORE = 100
MIN_SCORE = 0
INITAL_SCORE = 10
REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_PASSWORD = None
REDIS_KEY = 'proxies'


class RedisClient(object):
    # 初始化数据库
    def __init__(self):
        self.db = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD, decode_responses=True)

    # 添加代理
    def add(self, proxy, score=INITAL_SCORE):
        # 如果要添加的代理不在有序集合中则添加并初始化分数后返回
        # redis.zscore()用于返回proxy中的分数(这里不在有序集合中所以返回null)
        if not self.db.zscore(REDIS_KEY, proxy):
            # zadd()方法更新为redis.zadd(name, {value: score})
            return self.db.zadd(REDIS_KEY, {proxy: score})

    def random(self):
        """
        优先返回分数最高的代理;
        如果不存在最高,则按照分数排名随机返回一个
        :return:一个随机代理
        """
        # 返回范围内最高分的代理
        result = self.db.zrangebyscore(REDIS_KEY, MAX_SCORE, MAX_SCORE)
        if len(result):
            return random.choice(result)
        else:
            result = self.db.zrevrange(REDIS_KEY, 0, 100)
            if len(result):
                return random.choice(result)
            else:
                raise PoolEmptyError

    def decrease(self, proxy):
        """
        代理分数减一,如果小于最小分数则删除
        :param proxy: 代理
        :return: 修改之后的分数
        """
        score = self.db.zscore(REDIS_KEY, proxy)
        if score and score > MIN_SCORE:
            print('代理', proxy, '当前分数', score, '减1')
            # return self.db.zincrby(REDIS_KEY, proxy, -1)
            # zincrby()方法更新
            return self.db.zincrby(REDIS_KEY, -1, proxy)
        else:
            print('代理', proxy, '当前分数', score, '删除')
            return self.db.zrem(REDIS_KEY, proxy)

    def exists(self, proxy):
        """

        :param proxy: daili
        :return:是否存在
        """
        return not self.db.zscore(REDIS_KEY, proxy) == None

    def max(self, proxy):
        print('代理', proxy, '可用', '设置为', MAX_SCORE)
        return self.db.zadd(REDIS_KEY, {proxy: MAX_SCORE})

    def count(self):
        return self.db.zcard(REDIS_KEY)

    def all(self):
        return self.db.zrangebyscore(REDIS_KEY, MIN_SCORE, MAX_SCORE)


