'''
Description: 
email: 359066432@qq.com
Author: lhj
software: vscode
Date: 2021-10-04 18:46:56
platform: windows 10
LastEditors: lhj
LastEditTime: 2021-10-05 12:30:57
'''
from django.contrib import admin
# Register your models here.
from django.contrib import admin
from home.models import *
from django.apps import apps
# Register your models here.
app_models=apps.get_app_config('home').get_models()
for model in app_models:
    admin.site.register(model)