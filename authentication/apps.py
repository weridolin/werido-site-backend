'''
Description: 
email: 359066432@qq.com
Author: lhj
software: vscode
Date: 2021-09-11 15:01:27
platform: windows 10
LastEditors: lhj
LastEditTime: 2021-09-12 14:46:12
'''
from django.apps import AppConfig


class AuthenticationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'authentication'

    def ready(self) -> None:
        # 注册所有signals
        import authentication.v1.singals
        return super().ready(),