'''
Description: 
email: 359066432@qq.com
Author: lhj
software: vscode
Date: 2021-10-04 18:46:56
platform: windows 10
LastEditors: lhj
LastEditTime: 2021-10-05 12:30:31
'''
from django.apps import AppConfig
import etcd3
import uuid

class HomeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'home'

    # def ready(self):
        # ## 注册到 etcd  #todo 1集群？ 2 用gunicorn部署时每个worker会都会运行一段注册逻辑？注册逻辑放在master进程中？
        # from core import settings
        # etcd = etcd3.client(host=settings.ETCD_HOST, port=settings.ETCD_PORT)
        # id = str(uuid.uuid4())
        # etcd.put(f'/site/withoutauth/home/rest/{id}', 'http://home:8000')
