# -*- coding: utf-8 -*-
# @File  : scheduler.py
# @Author: AaronJny
# @Date  : 18-12-14 上午11:41
# @Desc  : 调度中心，所有组件在这里被统一启动和调度

import utils
import settings
from get_ip import ZdyIpGetter
from delele_ip import ExpireIpCleaner
from web_api import app
from squid_keeper import SquidKeeper
from multiprocessing import Process
import time


class Scheduler:
    logger = utils.get_logger('Scheduler')

    @staticmethod
    def fetch_ip():
        """
        获取新ip的进程
        :return:
        """
        while True:
            try:
                ZdyIpGetter().main()
            except Exception as e:
                print(e.args)

    @staticmethod
    def clean_ip():
        """
        定期清理过期ip的进程
        :return:
        """
        while True:
            try:
                ExpireIpCleaner().main()
            except Exception as e:
                print(e.args)

    @staticmethod
    def squid_keep():
        """
        维持squid使用最新ip的进程
        :return:
        """
        while True:
            try:
                SquidKeeper().main()
            except Exception as e:
                print(e.args)

    @staticmethod
    def api():
        """
        提供web接口的进程
        :return:
        """
        app.run('0.0.0.0', settings.API_WEB_PORT)

    def run(self):
        process_list = []

        try:
            # 只启动打开了开关的组件
            if settings.IP_GETTER_OPENED:
                # 创建进程对象
                fetch_ip_process = Process(target=Scheduler.fetch_ip)
                # 并将组件进程加入到列表中，方便在手动退出的时候杀死
                process_list.append(fetch_ip_process)
                # 开启进程
                fetch_ip_process.start()

            if settings.EXPIRE_IP_CLEANER_OPENED:
                clean_ip_process = Process(target=Scheduler.clean_ip)
                process_list.append(clean_ip_process)
                clean_ip_process.start()

            if settings.SQUID_KEEPER_OPENED:
                squid_keep_process = Process(target=Scheduler.squid_keep)
                process_list.append(squid_keep_process)
                squid_keep_process.start()

            if settings.WEB_API_OPENED:
                api_process = Process(target=Scheduler.api)
                process_list.append(api_process)
                api_process.start()
            # 一直执行，直到收到终止信号
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            # 收到终止信号时，关闭所有进程后再退出
            self.logger.info('收到终止信号，正在关闭所有进程...')
            for process in process_list:
                if process.is_alive():
                    process.terminate()
            self.logger.info('关闭完成！结束程序！')


if __name__ == '__main__':
    Scheduler().run()
