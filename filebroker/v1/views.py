
# Create your views here.
from email.policy import HTTP
from rest_framework.views import APIView
from rest_framework.response import Response
from filebroker.v1.serialziers import FileInfoSerializer
from filebroker.utils import generate_file_key
import datetime,json
from rest_framework import status
from filebroker.models import FileInfo,get_merge_file_path
import json
from core import settings
import os
from django.contrib.auth.models import User
from  django.http import FileResponse
# from django.utils.http import urlquote
from urllib.parse import urlencode,quote
# from urllib.parse import 
from filebroker.utils import is_expired
from celery_app.tasks import remove_file
from utils.http_ import HTTPResponse


class FileOperationViews(APIView):
    
    def get(self, request):
        # if not request.user.is_authenticated:
        #     return HttpResponseForbidden("please login first")
        ## 下载文件
        download_code = request.query_params.get("down_code",None)
        print(">>> down load file",{download_code})
        if not download_code:
            return HTTPResponse(
                    code=-1,
                    status=status.HTTP_400_BAD_REQUEST,
                    message=f"download_code can not be None",
                    app_code="filebroker"
            )  
        else:
            record:FileInfo = FileInfo.objects.filter(download_code=download_code,is_merge=True).first()
            if not record:
                return HTTPResponse(
                    code=-1,
                    status=status.HTTP_404_NOT_FOUND,
                    message=f"can not find file!",
                    app_code="filebroker"
                )  
            response = FileResponse(record.file.open(mode="rb"),filename=record.file_name)
            response['Content-Length'] = record.file.size      
            response['Content-Type'] = "application/octet-stream"
            response['Content-Disposition'] = f'attachment; filename="{quote(record.file_name)}"'
        return response

    def post(self,request):
        ## 初始化文件上传信息
        if not request.user.is_authenticated:
            user = User.objects.get(id=2)
        else:
            user = request.user
        ## 先判断是否已经存在，是的直接返回下载码:
        md5 = request.data.get("md5",None)
        if md5:
            try:
                record:FileInfo = FileInfo.objects.filter(md5=md5,is_merge=True).first()
                if record:
                    is_expire,timedelta = is_expired(record=record)
                    if is_expire:
                        ## delete expire record
                        file_path = os.path.join(settings.MEDIA_ROOT,record.file.name)
                        remove_file.delay(file_path)
                    else:
                        return HTTPResponse(data={
                            "file_info":FileInfoSerializer(record).data,
                            "is_exist":True,
                            "timedelta":timedelta,
                            },
                        status=status.HTTP_200_OK)                
            except FileInfo.DoesNotExist:
                pass  
        key = generate_file_key()
        params = request.data.copy()
        params.update({
            "file_key":key,
            "expire_time":datetime.datetime.now()+datetime.timedelta(hours=request.data.get("expire",24)),
        })
        serializer = FileInfoSerializer(data=params)
        if not serializer.is_valid():
            return HTTPResponse(message={'error':serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        else:
            file_info_list =[]
            for index in range(request.data.get("chunk_count")):
                params.update({"chunk_num":index})
                file_info_list.append(FileInfo(user=user,**params))
            FileInfo.objects.bulk_create(file_info_list)
            return HTTPResponse(data={"key":key,"is_exist":False},status=status.HTTP_200_OK)

    def put(self,request):
        ### 上传文件切片
        file_key = request.data.get("key",None)
        chunk_num = request.data.get("chunk_num",None)
        # chunk_count = request.data.get("chunk_count",None)
        file_name  = request.data.get("file_name",None)
        md5 = request.data.get("md5",None)
        if not file_key or not chunk_num or not file_name or not md5:
            return HTTPResponse(
                    code=-1,
                    status=status.HTTP_400_BAD_REQUEST,
                    message=f"file_key,chunk_num,file_name ,md5 can not be None",
                    app_code="filebroker"
            )  
        else:
            try:
                record:FileInfo = FileInfo.objects.filter(file_key=file_key,chunk_num=chunk_num,file_name=file_name).first()
                if not record:
                    return HTTPResponse(
                        code=-1,
                        status=status.HTTP_404_NOT_FOUND,
                        message=f"please upload file info first!",
                        app_code="filebroker"
                    )                     
            except FileInfo.DoesNotExist:
                return HTTPResponse(
                        code=-1,
                        status=status.HTTP_404_NOT_FOUND,
                        message=f"please upload file info first!",
                        app_code="filebroker"
                )  
        try:
            record.file = request.data.get('file')
        except KeyError:
            record.file = request.FILES['file']
        record.md5 = md5
        record.is_upload_finish = True
        record.save()
        return HTTPResponse(message="upload success!")


from rest_framework.decorators import api_view

@api_view(http_method_names=["POST"])
def generate_download_code(request):
    ### 合并文件并生成对应的下载码
    file_key=request.data.get("file_key",None)
    if not file_key:
        return HTTPResponse(
                code=-1,
                status=status.HTTP_400_BAD_REQUEST,
                message=f"file_key can not be None!",
                app_code="filebroker"
        )       
    down_code = generate_file_key()[:5]
    print("generate download code",down_code)
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
        return HTTPResponse(data={"code":down_code},status=status.HTTP_200_OK)
    except FileInfo.DoesNotExist:
        return HTTPResponse(
                code=-1,
                status=status.HTTP_404_NOT_FOUND,
                message=f"can not find file! please re upload",
                app_code="filebroker"
        )
    except Exception as exc:
        return HTTPResponse(
                code=-1,
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                message=f"serve error when generate down load code:{str(exc)}",
                app_code="filebroker"
        )
 

@api_view(http_method_names=["GET"])
def search_by_down_code(request,download_code=None):
    if not download_code:
        return HTTPResponse(
            code=-1,
            status=status.HTTP_400_BAD_REQUEST,
            message="bad request:download_code can not be None",
            app_code="filebroker"
        )
    else:
        records = FileInfo.objects.filter(download_code=download_code,is_merge=True).all()
        if len(records)>1:
            return HTTPResponse(
                code=-1,
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                message="find more than one file!",
                app_code="filebroker"
            )
        res = FileInfoSerializer(records,many=True).data
        return HTTPResponse(data=res,status=status.HTTP_200_OK)

