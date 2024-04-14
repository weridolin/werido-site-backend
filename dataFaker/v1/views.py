
'''
    faker数据生成器
        客户端配置生成数据字段(包括类型，条件)和生成的数据条数 ---(post)---> 后台生成对应的记录（返回这次数据对应的唯一key） ----> 客户端拿到key,
        建立WS连接----> 后台开始开始生成对应的 faker 数据并且通过WS实时反馈进度------> 生成完成，返回成功，断开WS，返回下载码 -------> 客户端通过
        下载码下载对应的文件


'''
# Create your views here.

from email.message import Message
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponseBadRequest,HttpResponseForbidden, HttpResponseNotFound,HttpResponseServerError
import datetime,json
from rest_framework import status
import json
from core import settings
import os
from django.contrib.auth.models import User
from  django.http import FileResponse
from rest_framework.decorators import action
# from django.utils.http import urlquote
from urllib.parse import unquote
from celery_app.tasks import remove_file
from filebroker.utils import generate_file_key
from dataFaker.models import DataFakerRecordInfo,upload_path
from dataFaker.v1.serializers import DataFakerRecordInfoSerializer
from utils.http_ import HTTPResponse
from utils.jwt import generate_jwt_token
from authenticationV1 import V1Authentication

import uuid
class FakerRecord(APIView):
    authentication_classes = [V1Authentication]
    permission_classes = []

    def get(self, request):
        # if not request.user.is_authenticated:
        #     return HttpResponseForbidden("please login first")
        ## 下载文件
        download_code = request.query_params.get("download_code",None)
        if not download_code:
            return HttpResponseBadRequest(content=f"bad request:download_code can not be None")
        else:
            record:DataFakerRecordInfo = DataFakerRecordInfo.objects.filter(
                download_code=download_code,is_finish=True).first()
            if not record:
                return HttpResponseNotFound(">>> can not find file!")
            response = FileResponse(record.file.open(mode="rb"),filename=f"{record.record_key}.csv")
            response['Content-Length'] = record.file.size      
            response['Content-Type'] = "application/octet-stream"
            response['Content-Disposition'] = f'attachment; filename="{unquote(f"{record.record_key}.csv")}"'
        return response

    def post(self,request):
        ## 初始化record生成信息
        if not request.user.is_authenticated:
            user = User.objects.get(id=2)
        else:
            user = request.user
        ## 先判断是否已经存在，是的直接返回下载码:
        fields = request.data.get("fields",[])
        count = request.data.get("count",0)
        if len(fields)==0 or count==0:
            return HTTPResponse(
                message=f"bad request:fields can not be None and count cannot be None OR 0",
                code=-1,
                status=status.HTTP_400_BAD_REQUEST,
                app_code="dataFaker")
        record_key = generate_file_key()
        record:DataFakerRecordInfo =DataFakerRecordInfo(
            expire_time = datetime.datetime.now()+datetime.timedelta(hours=request.data.get("expire",24)),
            user = user,
            fields=fields,
            count =count,
            record_key =record_key,
        )
        record.save()
        relative_path = upload_path(instance=record)
        ## 生成 websocket token
        payload = {
            "record_key":record_key,
            "user_id":user.id,
            "app":"site.alinlab.datafaker",
            "exp": (datetime.datetime.now() + datetime.timedelta(days=1)).timestamp(),
            "websocket_id": str(uuid.uuid4()),
            "target_path": os.path.join(settings.MEDIA_ROOT,relative_path), 
            "data_count" : count,
            "fields_info":fields,
            "callback_url_grpc":f"svc-site-oldbackend:50001"   
        }
        token = generate_jwt_token(payload,settings.JWT_KEY,algorithm="HS256")

        return HTTPResponse(data={
            "key":record_key,
            "is_exist":False,
            "websocket_url":f"wss://www.weridolin.cn/ws-endpoint/api/v1/?token={token}"
        },status=status.HTTP_200_OK,app_code="dataFaker")

from rest_framework.decorators import api_view
        

@api_view(http_method_names=["GET"])
def search_by_down_code(request,download_code=None):
    if not download_code:
        return HttpResponseBadRequest(content=f"bad request:download_code can not be None")
    else:
        try:
            record = DataFakerRecordInfo.objects.filter(download_code=download_code,is_finish=True).first()
        except DataFakerRecordInfo.DoesNotExist:
            return HTTPResponse(message="find more than one file!",status=status.HTTP_400_BAD_REQUEST,app_code="dataFaker",code=-1)
        res = DataFakerRecordInfoSerializer(record).data
        return HTTPResponse(data=res,status=status.HTTP_200_OK,app_code="dataFaker")

