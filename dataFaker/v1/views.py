
'''
    faker数据生成器
        客户端配置生成数据字段(包括类型，条件)和生成的数据条数 ---(post)---> 后台生成对应的记录（返回这次数据对应的唯一key） ----> 客户端拿到key,
        建立WS连接----> 后台开始开始生成对应的 faker 数据并且通过WS实时反馈进度------> 生成完成，返回成功，断开WS，返回下载码 -------> 客户端通过
        下载码下载对应的文件


'''



# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponseBadRequest,HttpResponseForbidden, HttpResponseNotFound,HttpResponseServerError
import datetime,json
from rest_framework import status
from filebroker.models import FileInfo,get_merge_file_path
import json
from core import settings
import os
from django.contrib.auth.models import User
from  django.http import FileResponse
from rest_framework.decorators import action
from django.utils.http import urlquote
from celery_app.tasks import remove_file
from filebroker.utils import generate_file_key
from dataFaker.models import DataFakerRecordInfo
from dataFaker.v1.serializers import DataFakerRecordInfoSerializer

class FakerRecord(APIView):
    
    def get(self, request):
        # if not request.user.is_authenticated:
        #     return HttpResponseForbidden("please login first")
        ## 下载文件
        download_code = request.query_params.get("download_code",None)
        if not download_code:
            return HttpResponseBadRequest(content=f"bad request:download_code can not be None")
        else:
            record:DataFakerRecordInfo = DataFakerRecordInfo.objects.filter(download_code=download_code,is_finish=True).first()
            if not record:
                return HttpResponseNotFound(">>> can not find file!")
            response = FileResponse(record.file.open(mode="rb"),filename=f"{record.record_key}.csv")
            response['Content-Length'] = record.file.size      
            response['Content-Type'] = "application/octet-stream"
            response['Content-Disposition'] = f'attachment; filename="{urlquote(f"{record.record_key}.csv")}"'
        return response

    def post(self,request):
        ## 初始化record生成信息
        if not request.user.is_authenticated:
            user = User.objects.get(id=1)
        else:
            user = request.user
        ## 先判断是否已经存在，是的直接返回下载码:
        fields = request.data.get("fields",[])
        count = request.data.get("count",0)
        if len(fields)==0 or count==0:
            return HttpResponseBadRequest(content=f"bad request:fields can not be None and count cannot be None OR 0")
        record_key = generate_file_key()
        record:DataFakerRecordInfo =DataFakerRecordInfo(
            expire_time = datetime.datetime.now()+datetime.timedelta(hours=request.data.get("expire",24)),
            user = user,
            fields=fields,
            count =count,
            record_key =record_key,
        )
        record.save()
        return Response(data={"key":record_key,"is_exist":False},status=status.HTTP_200_OK)

from rest_framework.decorators import api_view

@api_view(http_method_names=["POST"])
def generate_download_code(request):
    ### 合并文件并生成对应的下载码
    file_key=request.data.get("file_key",None)
    if not file_key:
        return HttpResponseBadRequest(content=f"bad request:file_key can not be None!")
    down_code = generate_file_key()[:5]
    print("generate dowload code",down_code)
    try:
        ## 合并文件
        records:list[FileInfo] = FileInfo.objects.filter(file_key=file_key).order_by("chunk_num").all()
        merge_file_path = get_merge_file_path(records[0],filename=records[0].file_name)
        target_file_path = os.path.join(settings.MEDIA_ROOT,merge_file_path)
        with open(target_file_path,"ab") as f:
            for record in records:
                with record.file.open(mode="rb") as slice_file:
                    for chunk in slice_file.chunks():
                        f.write(chunk)
        ## 提交删除文件的任务
        remove_file.delay([os.path.join(settings.MEDIA_ROOT,record.file.name) for record in records])
        ## 修改其中一条记录,并将多余的删除
        records[0].update(download_code=down_code,is_merge=True,file = merge_file_path)
        records[0].save()
        for record in records[1:]:
            record.delete()
        return Response(data={"code":down_code},status=status.HTTP_200_OK)
    except FileInfo.DoesNotExist:
        return HttpResponseNotFound("can not find file! please re upload")
    except Exception as exc:
        return HttpResponseServerError(content=f"serve error when generate down load code:{str(exc)}")
        

@api_view(http_method_names=["GET"])
def search_by_down_code(request,download_code=None):
    if not download_code:
        return HttpResponseBadRequest(content=f"bad request:download_code can not be None")
    else:
        records = DataFakerRecordInfo.objects.filter(download_code=download_code,is_finish=True).all()
        if len(records)>1:
            return HttpResponseServerError(content="find more than one file!")
        res = DataFakerRecordInfoSerializer(records,many=True).data
        return Response(data={"data":res},status=status.HTTP_200_OK)

