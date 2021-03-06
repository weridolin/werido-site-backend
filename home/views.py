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
from django.shortcuts import render, get_object_or_404, redirect

from articles.v1.serializers import *
from articles.models import *

from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from home.serializers import *
from home.models import *
from utils.helper import parse_ip



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

    def get_queryset(self):
        comments_list = SiteComments.objects.filter(is_valid=True).all()
        return comments_list

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


    def create(self, request, *args, **kwargs):
        print(request.data)
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            self.ip = x_forwarded_for.split(',')[0]
        else:
            self.ip = request.META.get('REMOTE_ADDR')
        if self.ip =="127.0.0.1":
            # ???????????????IP
            import socket
            self.ip = socket.gethostbyname(socket.gethostname())
        location = parse_ip(ip=self.ip)
        new_comment = SiteComments.objects.create(
            body = request.data.get("body",""),
            qq = request.data.get("qq",""),
            email = request.data.get("email",""),
            name = request.data.get("name",""),
            ip = self.ip,
            loc_province = location.get("regionName","????????????"),
            loc_country = location.get("country","????????????"),
            loc_city = location.get("city","????????????")
        )
        new_comment.save()
        return Response("created success!", status=status.HTTP_201_CREATED)


class UpdateLogViewSet(viewsets.ModelViewSet):
    serializer_class = UpdateLogSerializer
    queryset = UpdateLog.objects.all() # ??????????????????????????????????????????????????????



class FriendsLinksViewsApi(APIView):

    def get(self, request):
        links = FriendsLink.objects.filter(is_show=True)
        links_json = FriendsLinkSerializer(links, many=True)
        res = {
            "data": links_json.data
        }
        return Response(res, status=status.HTTP_200_OK)


class BackGroundMusicViews(APIView):

    def get(self, request):
        musicList = BackGroundMusic.objects.all()
        serializer = BackGroundMusicSerializer(musicList, many=True)

        res = {
            "data": serializer.data
        }
        return Response(res, status=status.HTTP_200_OK)
