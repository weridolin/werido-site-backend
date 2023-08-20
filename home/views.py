'''
Description: 
email: 359066432@qq.com
Author: lhj
software: vscode
Date: 2021-10-04 18:46:56
platform: windows 10
LastEditors: lhj
LastEditTime: 2021-10-06 21:04:48
'''
from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from rest_framework.response import Response
from home.serializers import *
from home.models import *
import json
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.views import APIView

from collections import OrderedDict
from rest_framework.pagination import PageNumberPagination
import json
from utils.models import CommentBrief
from django_redis import get_redis_connection
from redis.client import Redis

from rest_framework import mixins, viewsets
from django.shortcuts import render

# Create your views here.

from articles.v1.serializers import *
from articles.models import *

from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from home.serializers import *
from home.models import *
from utils.helper import parse_ip
from utils.http_ import HTTPResponse


from authenticationV1 import V1Authentication

class SiteCommentSetPagination(PageNumberPagination):
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


class SiteCommentViewsSet(viewsets.ModelViewSet):
    serializer_class = SiteCommentsSerializer
    pagination_class = SiteCommentSetPagination
    authentication_classes = [V1Authentication]


    def get_authenticators(self):
        if self.request.method == "GET":
            return []
        return super().get_authenticators()

    def get_queryset(self):
        comments_list = SiteComments.objects.filter(is_valid=True,replay_to=-1).all()
        return comments_list

    def list(self, request, *args, **kwargs):
        print(">>>get comment list")
        # queryset = SiteComments.objects.filter(is_valid=True,replay_to=-1).all()

        # page = self.paginate_queryset(queryset)
        # if page is not None:
        #     serializer = self.get_serializer(page, many=True)
        #     return self.get_paginated_response(serializer.data)

        # serializer = self.get_serializer(queryset, many=True)
        # return Response(serializer.data)
        response =  super().list(request,*args,**kwargs)
        return HTTPResponse(response.data,status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            self.ip = x_forwarded_for.split(',')[0]
        else:
            self.ip = request.META.get('REMOTE_ADDR')
        if self.ip =="127.0.0.1":
            # 获取本地的IP
            import socket
            self.ip = socket.gethostbyname(socket.gethostname())
        location = parse_ip(ip=self.ip)
        new_comment = SiteComments.objects.create(
            body = request.data.get("body",""),
            qq = request.data.get("qq",""),
            email = request.data.get("email",""),
            name = request.data.get("name",""),
            ip = self.ip,
            loc_province = location.get("regionName","未知省份"),
            loc_country = location.get("country","未知国家"),
            loc_city = location.get("city","未知城市")
        )
        new_comment.save()
        return HTTPResponse("created success!", status=status.HTTP_201_CREATED)

    @action(url_path="reply",methods=["get"],detail=True)
    def get_reply(self,request,pk=None):
        print("get reply list",pk)
        queryset = SiteComments.objects.filter(is_valid=True,root_id=pk).order_by("created").all()
        
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            res =  self.get_paginated_response(serializer.data)
            return HTTPResponse(res.data,status=status.HTTP_200_OK)

        serializer = self.get_serializer(queryset, many=True)
        # serializer = SiteCommentsSerializer(queryset,many=True)
        return HTTPResponse(serializer.data,status=status.HTTP_200_OK)

weekdays = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"]

class UpdateLogViewSet(viewsets.ModelViewSet):
    serializer_class = UpdateLogSerializer
    queryset = UpdateLog.objects.all() # 这里是针对所有的请求都会以这个为标准

    def list(self, request, *args, **kwargs):
        logs = UpdateLog.objects.all().order_by('-updated')
        res = dict()
        for log in logs:
            year_month = str(log.updated.year)+"-"+str(log.updated.month)
            day_weekday = str(log.updated.day)+"-"+weekdays[log.updated.weekday()]
            if year_month not in res:
                res[year_month] = dict()
            if day_weekday not in res[year_month]:
                res[year_month][day_weekday] = list()

            res[year_month][day_weekday].append(UpdateLogSerializer(log).data)
    
        return HTTPResponse(data=res,status=status.HTTP_200_OK)




class FriendsLinksViewsApi(APIView):

    def get(self, request,*args, **kwargs):
        links = FriendsLink.objects.all().order_by('updated')
        links_json = FriendsLinkSerializer(links, many=True).data
        return HTTPResponse(data=links_json,status=status.HTTP_200_OK)


class BackGroundMusicViews(APIView):

    def get(self, request):
        musicList = BackGroundMusic.objects.all()
        serializer = BackGroundMusicSerializer(musicList, many=True)
        return HTTPResponse(data=serializer.data, status=status.HTTP_200_OK)

