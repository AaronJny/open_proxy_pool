# -*- coding: utf-8 -*-
# @File  : web_api.py
# @Author: AaronJny
# @Date  : 18-12-14 上午11:22
# @Desc  : 提供http接口的web程序


import utils
import settings
import flask
import random
import time

redis_client = utils.get_redis_client()
ip_pool_key = settings.IP_POOL_KEY
app = flask.Flask(__name__)


@app.route('/random/')
def random_ip():
    """
    获取一个随机ip
    :return:
    """
    # 获取redis中仍可用的全部ip
    proxy_ips = redis_client.zrangebyscore(ip_pool_key, int(time.time()),
                                           int(time.time()) + settings.PROXY_IP_TTL * 10)
    if proxy_ips:
        ip = random.choice(proxy_ips)
        # 如果ip需要密码访问，则添加
        if settings.USE_PASSWORD:
            ip = '{}:{}@{}'.format(settings.USERNAME, settings.PASSWORD, ip.decode('utf8'))
        return ip
    else:
        return ''


@app.route('/total/')
def total_ip():
    """
    统计池中可用代理的数量
    :return:
    """
    total = redis_client.zcard(ip_pool_key)
    if total:
        return str(total)
    else:
        return '0'


def main():
    """
    程序运行入口
    :return:
    """
    app.run('0.0.0.0', port=settings.API_WEB_PORT)


if __name__ == '__main__':
    app.run('0.0.0.0', port=settings.API_WEB_PORT)
