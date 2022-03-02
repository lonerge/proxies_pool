# 4.接口模块:
# 提供远程获取代理服务

from flask import Flask, g
from db import RedisClient


__all__ = ['app']
app = Flask(__name__)

def get_conn():
    if not hasattr(g, 'redis'):
        g.redis = RedisClient()
    return g.redis

@app.route('/')
def index():
    conn = get_conn()
    num = str(conn.count())
    return '<h1>Welcome to Proxy Pool System<h1>\n' \
           '<a href="http://127.0.0.1:5000/random">随机获取一个代理</a>' \
           '\n<a href="http://127.0.0.1:5000/count">代理总数:{}</a>'.format(num)

    # return '<a href="http://127.0.0.1:5000/count">代理总数</a>'
    # return '<h1>Welcome to Proxy Pool System<h1>'

@app.route('/random')
def get_proxy():
    # 获取一个随机代理
    conn = get_conn()
    return conn.random()

@app.route('/count')
def get_count():
    # 获取代理总数
    conn = get_conn()
    return str(conn.count())


if __name__ == '__main__':
    app.run()



