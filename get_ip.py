# -*- coding: utf-8 -*-
# @File  : get_ip.py
# @Author: AaronJny
# @Date  : 18-12-14 上午10:44
# @Desc  : 从指定网站上获取代理ip,
#          我目前在使用站大爷，就以站大爷为例

import requests
import time
import utils
import settings
from gevent.pool import Pool
from gevent import monkey

monkey.patch_all()


class ZdyIpGetter:
    """
    从`站大爷`上提取代理ip的脚本，使用其他代理服务的可自行编写相关脚本，
    原理和逻辑都是相通的，部分细节上需要针对处理
    """

    def __init__(self):
        # 购买服务时，网站给出的提取ip的api，替换成自己的
        self.api_url = 'http://xxxxxxxxxxxxxxxxxxxxxxxxxx'
        self.logger = utils.get_logger(getattr(self.__class__, '__name__'))
        self.proxy_list = []
        self.good_proxy_list = []
        self.pool = Pool(5)
        self.server = utils.get_redis_client()

    def check_proxy(self, proxy):
        """
        检查代理是否可用，
        并将可用代理加入到指定列表中
        :param proxy:
        :return:
        """
        if settings.USE_PASSWORD:
            tmp_proxy = '{}:{}@{}'.format(settings.USERNAME, settings.PASSWORD, proxy)
        else:
            tmp_proxy = '{}'.format(proxy)
        proxies = {
            'http': 'http://' + tmp_proxy,
            'https': 'https://' + tmp_proxy,
        }
        try:
            # 验证代理是否可用时，访问的是ip138的服务
            resp = requests.get('http://2019.ip138.com/ic.asp', proxies=proxies, timeout=10)
            # self.logger.info(resp.content.decode('gb2312'))
            # 判断是否成功使用代理ip进行访问
            assert proxy.split(':')[0] in resp.content.decode('gb2312')
            self.logger.info('[GOOD] - {}'.format(proxy))
            self.good_proxy_list.append(proxy)
        except Exception as e:
            self.logger.info('[BAD] - {} , {}'.format(proxy, e.args))

    def get_proxy_list(self):
        """
        提取一批ip，筛选出可用的部分
        注：当可用ip小于两个时，则保留全部ip（不论测试成功与否）
        :return:
        """
        while True:
            try:
                res = requests.get(self.api_url, timeout=10).content.decode('utf8')
                break
            except Exception as e:
                self.logger.error('获取代理列表失败！重试！{}'.format(e))
                time.sleep(1)
        if len(res) == 0:
            self.logger.error('未获取到数据！')
        elif 'bad' in res:
            self.logger.error('请求失败！')
        # 检测未考虑到的异常情况
        elif res.count('.') != 15:
            self.logger.error(res)
        else:
            self.logger.info('开始读取代理列表！')
            for line in res.split():
                if ':' in line:
                    self.proxy_list.append(line.strip())
            self.pool.map(self.check_proxy, self.proxy_list)
            self.pool.join()
            # 当本次检测可用代理数量小于2个时，则认为检测失败，代理全部可用
            if len(self.good_proxy_list) < 2:
                self.good_proxy_list = self.proxy_list.copy()
            self.logger.info('>>>> 完成! <<<<')

    def save_to_redis(self):
        """
        将提取到的有效ip保存到redis中，
        供其他组件访问
        :return:
        """
        for proxy in self.good_proxy_list:
            self.server.zadd(settings.IP_POOL_KEY, int(time.time()) + settings.PROXY_IP_TTL, proxy)

    def fetch_new_ip(self):
        """
        获取一次新ip的整体流程控制
        :return:
        """
        self.proxy_list.clear()
        self.good_proxy_list.clear()
        self.get_proxy_list()
        self.save_to_redis()

    def main(self):
        """
        周期获取新ip
        :return:
        """
        start = time.time()
        while True:
            # 每 settings.FETCH_INTERVAL 秒获取一批新IP
            if time.time() - start >= settings.FETCH_INTERVAL:
                self.fetch_new_ip()
                start = time.time()
            time.sleep(2)


if __name__ == '__main__':
    ZdyIpGetter().main()
