'''
Description: 
email: 359066432@qq.com
Author: lhj
software: vscode
Date: 2021-09-06 00:04:32
platform: windows 10
LastEditors: lhj
LastEditTime: 2021-09-06 00:11:20
'''
from django.urls import path,re_path
from authentication.views import login

urlpatterns=[
    path("login/",login,name="login")
]