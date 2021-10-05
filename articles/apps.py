'''
Description: 
email: 359066432@qq.com
Author: lhj
software: vscode
Date: 2021-10-02 16:08:58
platform: windows 10
LastEditors: lhj
LastEditTime: 2021-10-02 23:42:07
'''
from django.apps import AppConfig


class ArticlesConfig(AppConfig):
    name = 'articles'

    def ready(self) -> None:
        # 注册所有signals
        import articles.v1.signals
        return super().ready()