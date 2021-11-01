'''
Description: 
email: 359066432@qq.com
Author: lhj
software: vscode
Date: 2021-05-16 12:32:46
platform: windows 10
LastEditors: lhj
LastEditTime: 2021-11-02 00:34:39
'''
# -*- encoding: utf-8 -*-
from django.urls import path,re_path
from rest_framework import routers
from articles.v2.views import ArticleViewsSet,TagViewsSet,TypesViewsSet

app_name="blog"

router = routers.SimpleRouter(trailing_slash=False)
router.register(r"articles",ArticleViewsSet,basename="articles")
router.register(r"articles_tags",TagViewsSet,basename="articles-tags")
router.register(r"articles_types",TypesViewsSet,basename="articles-types")
urlpatterns =[

]
urlpatterns += router.urls



