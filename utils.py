# -*- coding: utf-8 -*-
# @File  : utils.py
# @Author: AaronJny
# @Date  : 18-12-14 上午11:07
# @Desc  :

from redis import StrictRedis, ConnectionPool
import settings
import logging


def get_redis_client():
    """
    获取一个redis连接
    :return:
    """
    server_url = settings.REDIS_SERVER_URL
    return StrictRedis(connection_pool=ConnectionPool.from_url(server_url))


def get_logger(name=__name__):
    """
    获取一个logger，用以格式化输出信息
    :param name:
    :return:
    """
    logger = logging.getLogger(name)
    logger.handlers.clear()
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s: - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S')

    # 使用StreamHandler输出到屏幕
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    ch.setFormatter(formatter)

    logger.addHandler(ch)

    return logger
