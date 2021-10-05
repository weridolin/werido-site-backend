'''
Description: 
email: 359066432@qq.com
Author: lhj
software: vscode
Date: 2021-05-16 12:32:46
platform: windows 10
LastEditors: lhj
LastEditTime: 2021-10-05 12:46:49
'''
# -*- encoding: utf-8 -*-
from django.urls import path,re_path
from rest_framework import routers
from articles.v1.views import *

app_name="blog"

# router = routers.SimpleRouter()
# router.register(r"articleDetail",ArticleDetail)

urlpatterns=[

    path(r"articles",ArticleViews.as_view(),name="article-list"),

    # 正则表示式 ：(?P<name>pattern)  name为参数名 ，pattern 为表达式
    re_path(r"articles/(?P<pk>\d+)$",ArticleViews.as_view(),name="article-detail"),

    path(r"tags",TagsViews.as_view(),name="tags"),
    path(r"types",TypesViews.as_view(),name="types"),
    # # 文章搜索，返回简略信息
    # path(r"search/", Search.as_view(), name="article-search-brief"),



]


