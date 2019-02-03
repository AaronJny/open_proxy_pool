# -*- coding: utf-8 -*-
# @File  : settings.py
# @Author: AaronJny
# @Date  : 18-12-14 上午11:13
# @Desc  :

# 代理池redis键名
IP_POOL_KEY = 'open_proxy_pool'

# redis连接，根据实际情况进行配置
REDIS_SERVER_URL = 'redis://:your_password@your_host:port/db_name'

# api对外端口
API_WEB_PORT = 9102

# 代理是否需要通过密码访问,当此项为False时可无视USERNAME和PASSWORD的配置
USE_PASSWORD = True

# 用户名
# 注意：用户名密码是指代理服务方提供给你，用以验证访问授权的凭证。
# 无密码限制时可无视此项，并将USE_PASSWORD改为False
USERNAME = 'your_username'

# 密码
PASSWORD = 'your_password'

# ***********功能组件开关************

# 打开web api功能，不使用web api的话可以关闭
WEB_API_OPENED = True

# 打开squid代理转发服务的维持脚本，不使用squid的话可以关闭
SQUID_KEEPER_OPENED = True

# 打开清理过期ip的脚本，如果池内的代理ip永远不会失效的话可以关闭
EXPIRE_IP_CLEANER_OPENED = True

# 打开定时获取ip并检查的脚本，如果不需要获取新ip的话可以关闭
IP_GETTER_OPENED = True

# ***********************************

# 清理代理ip的频率，如下配置代表每两次之间间隔6秒
CLEAN_INTERVAL = 6

# 获取代理ip的频率，根据api的请求频率限制进行设置
# 比如`站大爷`的频率限制是10秒一次，我就设置成了12秒
FETCH_INTERVAL = 12

# squid从redis中加载新ip的频率
SQUID_KEEPER_INTERVAL = 12

# 代理ip的生命周期，即一个新ip在多久后将被删除，单位：秒
PROXY_IP_TTL = 60
