'''
Description: 
email: 359066432@qq.com
Author: lhj
software: vscode
Date: 2021-05-16 12:32:46
platform: windows 10
LastEditors: lhj
LastEditTime: 2021-11-02 00:30:50
'''
from json.decoder import JSONDecodeError
import re,json
from django.db.models import query
from django.db.models.query import QuerySet

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
        """文章检索，检索条件可以为:title/tag/type TODO:tag/type"""
        title = request.query_params.get("title", None)
        print(title)
        if title:
            article_list = Article.objects.filter(title__icontains=title).order_by("-created")
            serializer = ArticleBriefSerializer(article_list, many=True)
            print(serializer.data)
            # return ArticlePagination().get_paginated_response(data=serializer.data)
            return Response(serializer.data,status=status.HTTP_404_NOT_FOUND)
        else:
            return Response("not match found!",status=status.HTTP_404_NOT_FOUND)        


class TagViewsSet(ModelViewSet):
    queryset = Tags.objects.all()
    serializer_class = TagsSerializer
    
    def update(self, request, *args, **kwargs):
        """put 也改为部分更新"""
        return super().update(request,*args,partial=True,**kwargs)    

class TypesViewsSet(ModelViewSet):

    queryset = Types.objects.all()
    serializer_class = TypesSerializer 
    




