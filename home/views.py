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
from opentelemetry import trace
from opentelemetry.trace.propagation.tracecontext import TraceContextTextMapPropagator
from collections import OrderedDict
from rest_framework.pagination import PageNumberPagination
import json,os,sys
from utils.models import CommentBrief
from django_redis import get_redis_connection
from redis.client import Redis
from rest_framework import mixins, viewsets
from django.shortcuts import render
from django.http import FileResponse
# Create your views here.
import hashlib
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
from rpc.usercenter.client import get_user_info
from authenticationV1 import V1Authentication
from core.settings import ETCD_HOST,ETCD_PORT,USERCENTER_KEY,USERCENTER_SVC_NAME,USERCENTER_SVC_NAME_NAMESPACE
from utils.etcd_client import get_srv
import re

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
        user_id =  request.user

        # tracer = trace.get_tracer(__name__)
        # with tracer.start_as_current_span('begin-call-rpc'):
        #     carrier = dict()
        # TraceContextTextMapPropagator().inject(carrier)
        # ctx = (("traceparent",carrier.get('traceparent',None) or request.traceparent),)
        ctx = (("traceparent",request.traceparent),)
        user_center = get_srv(etcd_key=USERCENTER_KEY,srv_name=USERCENTER_SVC_NAME,namespace=USERCENTER_SVC_NAME_NAMESPACE)
        
        request.span.add_event("get user info by rpc",attributes={"usercenter.service":user_center,"user_id":user_id})
        user_info = get_user_info(user_id=user_id,target=f"{user_center}:8081",ctx=ctx)
        request.span.add_event("get user info finish",attributes={f"user_info:{user_info}"})
  
        print("user info: ",user_info)
        new_comment = SiteComments.objects.create(
            body = request.data.get("body",""),
            # qq = user_info.qq,
            user_id=user_id,
            email = user_info.userEmail,
            name = user_info.userName,
            ip = self.ip,
            loc_province = location.get("regionName","未知省份"),
            loc_country = location.get("country","未知国家"),
            loc_city = location.get("city","未知城市")
        )
        new_comment.save()
        return HTTPResponse("created success!", status=status.HTTP_201_CREATED)

    @action(url_path="reply",methods=["get","post"],detail=True)
    def get_reply(self,request,pk=None):
        if request.method.lower() == "get":
            # print("get reply list",pk)
            queryset = SiteComments.objects.filter(is_valid=True,root_id=pk).order_by("created").all()
            
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                res =  self.get_paginated_response(serializer.data)
                return HTTPResponse(res.data,status=status.HTTP_200_OK)

            serializer = self.get_serializer(queryset, many=True)
            # serializer = SiteCommentsSerializer(queryset,many=True)
            return HTTPResponse(serializer.data,status=status.HTTP_200_OK)
        elif request.method.lower()=="post":
            # print("回复评论",request.data)
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
            user_id =  request.user

            user_center = get_srv(etcd_key=USERCENTER_KEY,srv_name=USERCENTER_SVC_NAME,namespace=USERCENTER_SVC_NAME_NAMESPACE)
            user_info = get_user_info(user_id=user_id,target=user_center)
            print("user info: ",user_info)
            new_comment = SiteComments.objects.create(
                body = request.data.get("body",""),
                root_id = pk,
                replay_to = request.data.get("replay_to",-1),
                # qq = user_info.qq,
                email = user_info.userEmail,
                name = user_info.userName,
                ip = self.ip,
                loc_province = location.get("regionName","未知省份"),
                loc_country = location.get("country","未知国家"),
                loc_city = location.get("city","未知城市")
            )
            new_comment.save()
            return HTTPResponse(message="评论成功!")

weekdays = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"]

class UpdateLogViewSet(viewsets.ModelViewSet):
    serializer_class = UpdateLogSerializer
    queryset = UpdateLog.objects.all() # 这里是针对所有的请求都会以这个为标准
    authentication_classes = [V1Authentication]

    def get_authenticators(self):
        if self.request.method == "GET":
            return []
        return super().get_authenticators()


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


    def create(self, request, *args, **kwargs):
        """
            提交一个更新日志
            {
                "repo_uri":"更新日志仓库",
                "commit_content":"更新日志内容",
                "author":"更新日志作者",
                "is_finish":false,
                "commit_id":"提交的commit_id",
                "finish_time":"2023-09-03 01:03:11"
            }

            commit_content: 提交内容的格式:
                message:Xxx
                author:xxx
        """
        commit_content = request.data.pop("commit_content",None)
        

        print("commit_content",commit_content,"request body",request.data)
        if not commit_content:
            return HTTPResponse(message="提价内容不能为空!",status=status.HTTP_400_BAD_REQUEST)
        message,author = re.findall(r"message:([\s\S]*)author:([\s\S]*)",commit_content)[0]
        print("message",message,"author",author)
        serializer = UpdateLogSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(**{"commit_content":message.replace('\n', '').replace('\r', ''),
                "user_name":author.replace('\n', '').replace('\r', ''),
                "commit_message":message.replace('\n', '').replace('\r', ''),
                "user_id":1})
            return HTTPResponse(data=serializer.data,status=status.HTTP_201_CREATED)
        print("create update log error",serializer.errors)
        return HTTPResponse(message="提交失败!",status=status.HTTP_400_BAD_REQUEST)


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

from django.http import HttpResponse
from django.utils.cache import get_conditional_response
from django.utils.http import http_date, quote_etag

class BackImagesViews(viewsets.ModelViewSet):
    serializer_class = BackGroundImagesSerializer
    queryset = BackGroundImages.objects.all()
    authentication_classes = []

    def list(self, request):
        imagesList = BackGroundImages.objects.filter(is_able=True).all()
        # for image in imagesList:
        #     filename = image.path.split("/")[-1]
        #     file_path = os.path.join(os.path.dirname(__file__),"bgList",filename)
        #     with open(file_path,"rb") as f:
        #         image.md5 = hashlib.md5(f.read()).hexdigest()
        #         image.file_name = filename
        #         image.save()
        serializer = BackGroundImagesSerializer(imagesList, many=True)
        return HTTPResponse(data=serializer.data, status=status.HTTP_200_OK)
    

    @action(url_path="detail/(?P<file_name>\S+)",methods=["get"],detail=False,url_name="GetImage")
    def get_image(self,request,file_name=None):
        print("get image",file_name)
        if not file_name:
            return HTTPResponse(message="图片名称不能为空!",status=status.HTTP_400_BAD_REQUEST)
        # 判断文件是否存在,
        bg = BackGroundImages.objects.filter(file_name=file_name,is_able=True).first()
        if not bg or not os.path.exists(os.path.join(os.path.dirname(__file__),"bgList",file_name)):
            return HTTPResponse(message="图片不存在!",status=status.HTTP_404_NOT_FOUND)
        else:
            timestamps = os.path.getmtime(os.path.join(os.path.dirname(__file__),"bgList",file_name))
            dt = datetime.datetime.fromtimestamp(timestamps)
            if not timezone.is_aware(dt):
                dt = timezone.make_aware(dt, timezone.utc)
            last_modified = int(dt.timestamp())
            etag = quote_etag(bg.md5)
            response = get_conditional_response(
                request,
                etag=etag,
                last_modified=last_modified,
            )
            if not response:
                with open(os.path.join(os.path.dirname(__file__),"bgList",file_name),"rb") as f:
                    image = f.read()

                header = {
                    "Cache-Control":"max-age=60*60",
                    "Last-Modified":http_date(last_modified),
                    "ETag":etag
                }
                return HttpResponse(image,content_type='image/*',headers=header)
            else:
                response.headers["Cache-Control"] = "max-age=60*60"
                if not response.has_header("Last-Modified"):
                    response.headers["Last-Modified"] = http_date(last_modified)
                if etag:
                    response.headers.setdefault("ETag", etag)
                return response  # 资源未过期 直接返回304
        # redis_conn:Redis = get_redis_connection("default")
        # image = redis_conn.get(file_name)
        # if not image:
        #     return HTTPResponse(message="图片不存在!",status=status.HTTP_404_NOT_FOUND)
        # return HTTPResponse(data=image,status=status.HTTP_200_OK)

