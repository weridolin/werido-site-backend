'''
Description: 
email: 359066432@qq.com
Author: lhj
software: vscode
Date: 2021-10-02 17:59:06
platform: windows 10
LastEditors: lhj
LastEditTime: 2021-10-02 18:19:03
'''
from django.db import models
from django.utils import timezone

TypesChoice=[
    ("article","article"),
    ("project","project")
]

class BaseModel(models.Model):
    created = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated = models.DateTimeField(auto_now=True, verbose_name='修改时间')

    class Meta:
        app_label = 'Base'
        managed = False 
        abstract = True


from rest_framework import serializers

class BaseSerializer(serializers.ModelSerializer):
    created = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    updated = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)



from django.http import HttpResponse


class ResponseWithCallback(HttpResponse):

    def close(self) -> None:
        super().close()
        