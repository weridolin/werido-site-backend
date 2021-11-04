'''
Description: 
email: 359066432@qq.com
Author: lhj
software: vscode
Date: 2021-05-16 12:32:46
platform: windows 10
LastEditors: lhj
LastEditTime: 2021-11-05 00:52:45
'''
# from _typeshed import Self
from json.decoder import JSONDecodeError
import re,json
import typing_extensions
from django.db.models import query
from django.db.models.query import QuerySet
import django_filters

from rest_framework.settings import IMPORT_STRINGS
from articles.v1.serializers import *
from articles.models import *
# Create your views here.
from rest_framework.exceptions import UnsupportedMediaType
from django.http import Http404,HttpResponseBadRequest,HttpResponseNotFound,HttpResponseNotAllowed
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from articles.utils import model2json
from rest_framework.parsers import JSONParser,FormParser
from rest_framework.decorators import parser_classes
from articles.v1.signals import update_pre_and_next,update_pre_and_next_signal
from collections import OrderedDict

from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import action
class ArticlePagination(PageNumberPagination):
    page_size = 6
    page_size_query_param = 'size'
    page_query_param = 'page'

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('count', self.page.paginator.count),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('last_page', self.get_last_page()),
            ('results', data)

        ]))

    def get_last_page(self):
        index = int(self.page.paginator.count/self.get_page_size(self.request)) if self.page.paginator.count % self.get_page_size(
            self.request) == 0 else int(self.page.paginator.count/self.get_page_size(self.request)+1)
        return index    

from django_filters import FilterSet
class ArticleFilterSet(FilterSet):
    # title 为 request get的字段 
    title = django_filters.CharFilter(lookup_expr="icontains", field_name = "title")
    # _type =django_filters.CharFilter(lookup_expr="icontains", field_name = "type_name")
    type = django_filters.CharFilter(lookup_expr="icontains", field_name = "type__name")
    tags = django_filters.CharFilter(lookup_expr="icontains", field_name = "tags__name")
    class Meta:
        model = Article
        fields = ["title", "type__name","tags__name"]

from django_filters.rest_framework import  DjangoFilterBackend
class ArticleViewsSet(ModelViewSet):
    """文章接口"""

    parser_classes=[JSONParser]
    page = 1
    default_page_num = 6
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer 
    pagination_class = ArticlePagination


    def update(self, request, *args, **kwargs):
        """put 也改为部分更新"""
        return super().update(request,*args,partial=True,**kwargs)

    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @action(methods=["GET"],detail=False,url_name="article-search")
    def search(self,request):
        """文章检索，检索条件可以为:title/tag/type """
        print(request.query_params)
        filter_article_list = ArticleFilterSet(request.query_params,queryset=self.get_queryset()).qs
        serializer = ArticleBriefSerializer(filter_article_list, many=True)
        # return ArticlePagination().get_paginated_response(data=serializer.data)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    @action(methods=["GET"],detail=False,url_name="article-count")
    def count(self,request):
        """统计文章总数，检索条件可以为:title/tag/type """
        filter_article_list = ArticleFilterSet(request.query_params,queryset=self.get_queryset()).qs
        return Response({"count":len(filter_article_list)},status=status.HTTP_200_OK)
  


class TagViewsSet(ModelViewSet):
    queryset = Tags.objects.all()
    serializer_class = TagsSerializer
    
    def update(self, request, *args, **kwargs):
        """put 也改为部分更新"""
        return super().update(request,*args,partial=True,**kwargs)    

class TypesViewsSet(ModelViewSet):

    queryset = Types.objects.all()
    serializer_class = TypesSerializer 
    




