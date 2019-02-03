# -*- coding: utf-8 -*-
# @File  : delele_ip.py
# @Author: AaronJny
# @Date  : 18-12-14 上午11:15
# @Desc  : 过期ip清理器


import utils
import settings
import time


class ExpireIpCleaner:

    def __init__(self):
        self.logger = utils.get_logger(getattr(self.__class__, '__name__'))
        self.server = utils.get_redis_client()

    def clean(self):
        """
        清理代理池中的过期ip
        :return:
        """
        self.logger.info('开始清理过期ip')
        # 计算清理前代理池的大小
        total_before = int(self.server.zcard(settings.IP_POOL_KEY))
        # 清理
        self.server.zremrangebyscore(settings.IP_POOL_KEY, 0, int(time.time()))
        # 计算清理后代理池的大小
        total_after = int(self.server.zcard(settings.IP_POOL_KEY))
        self.logger.info('完毕！清理前可用ip {}，清理后可用ip {}'.format(total_before, total_after))

    def main(self):
        """
        周期性的清理过期ip
        :return:
        """
        while True:
            self.clean()
            self.logger.info('*' * 40)
            time.sleep(settings.CLEAN_INTERVAL)


if __name__ == '__main__':
    ExpireIpCleaner().main()
