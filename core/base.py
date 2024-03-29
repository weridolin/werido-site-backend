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
from rest_framework.pagination import PageNumberPagination
from rest_framework import serializers
from django.db import models
from rest_framework.response import Response
from utils.http_ import HTTPResponse
from collections import OrderedDict
import datetime

TypesChoice = [
    ("article", "article"),
    ("project", "project")
]


class BaseModel(models.Model):
    created = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated = models.DateTimeField(auto_now=True, verbose_name='修改时间')

    class Meta:
        app_label = 'Base'
        managed = False
        abstract = True


class BaseSerializer(serializers.ModelSerializer):
    created = serializers.DateTimeField(
        format="%Y-%m-%d %H:%M:%S", read_only=True)
    updated = serializers.DateTimeField(
        format="%Y-%m-%d %H:%M:%S", read_only=True)


# class ResponseWithCallback(HttpResponse):

#     def close(self) -> None:
#         super().close()

## 统一下返回格式
class PageNumberPaginationWrapper(PageNumberPagination):
    page_size=20
    page_size_query_param="page_size"
    max_page_size=50

    def get_paginated_response(self, data):
        response= Response(OrderedDict([
            ('count', self.page.paginator.count),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('results', data),
            ('page', self.request.query_params.get(self.page_query_param, 1))
        ]))

        return HTTPResponse(
            data=response.data
        )


from rest_framework.filters import OrderingFilter
class  OrderingFilterWrapper(OrderingFilter):
    ordering_fields = ordering = ['id']
    ordering_param = "sort"