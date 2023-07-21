# gunicorn.conf
import multiprocessing
import os,sys


# 并行工作进程数
# workers = multiprocessing.cpu_count() * 2 + 1
workers = 1
# 指定每个工作者的线程数
threads = 2
# 监听内网端口5000
bind = '0.0.0.0:8001'
# 设置守护进程,将进程交给supervisor管理
daemon = 'false'
# 工作模式协程
# worker_class = 'gevent' # 只支持WSGI
worker_class = 'uvicorn.workers.UvicornWorker' # 支持ASGI
# 设置最大并发量
worker_connections = 1000
# 设置进程文件目录
pidfile = '/usr/gunicorn.pid'
# 设置访问日志和错误信息日志路径
accesslog = '/usr/gunicorn_acess.log'
errorlog = '/usr/gunicorn_error.log'
# 设置日志记录水平
loglevel = 'info'
