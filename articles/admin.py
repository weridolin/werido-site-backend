'''
Description: 
email: 359066432@qq.com
Author: lhj
software: vscode
Date: 2021-10-02 16:08:58
platform: windows 10
LastEditors: lhj
LastEditTime: 2021-10-02 17:39:28
'''
from django.contrib import admin
from articles.models import *
from django.apps import apps
# Register your models here.
app_models=apps.get_app_config('articles').get_models()
for model in app_models:
    admin.site.register(model)
