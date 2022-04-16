
import os
from statistics import mode

from core import settings
from django.db import models
from core.base import BaseModel
from django.contrib.auth.models import User
# Create your models here.

def file_directory_path(instance, filename):
    target_path = 'file/user_{0}/{1}/{2}{3}'.format(instance.user.id,instance.file_key,filename,instance.chunk_num)
    if os.path.exists(os.path.join(settings.MEDIA_ROOT,target_path)):
        os.remove(os.path.join(settings.MEDIA_ROOT,target_path))
    return 'file/user_{0}/{1}/{2}{3}'.format(instance.user.id,instance.file_key,filename,instance.chunk_num)

def get_merge_file_path(instance, filename):
    target_path = 'file/user_{0}/{1}/{2}'.format(instance.user.id,instance.file_key,filename)
    if os.path.exists(os.path.join(settings.MEDIA_ROOT,target_path)):
        os.remove(os.path.join(settings.MEDIA_ROOT,target_path))
    return 'file/user_{0}/{1}/{2}'.format(instance.user.id,instance.file_key,filename)

class FileInfo(BaseModel):
    # 上传时第一步会发送一个POST请求会生成一个唯一KEY
    file_key = models.CharField(max_length=255,verbose_name="文件唯一标识",null=False,db_index=True)
    file_name = models.CharField(max_length=128,null=False,verbose_name="文件名")
    user = models.ForeignKey(to=User,verbose_name="文件上传所属用户",on_delete=models.CASCADE,null=True)
    file_size = models.BigIntegerField(null=True,verbose_name="文件大小(kb)")
    is_delete = models.BooleanField(verbose_name="是否删除",default=False)
    expire_time = models.DateTimeField(verbose_name="过期时间",null=False)
    file = models.FileField(max_length=255, upload_to=file_directory_path,null=True)
    md5 = models.CharField(max_length=255,verbose_name="文件MD5",null=True,db_index=True)
    is_upload_finish = models.BooleanField(verbose_name="是否已经上传完成",default=False)
    is_last = models.BooleanField(verbose_name="是否为最后一个切片",default=False)
    chunk_num = models.SmallIntegerField(verbose_name="文件切片序号",null=False,default=0)
    chunk_count = models.IntegerField(verbose_name="文件切片总数",null=False)
    download_code = models.CharField(max_length=255,verbose_name="文件下载码",null=True)
    is_merge = models.BooleanField(verbose_name="是否已经合并",default=False)

    class Meta:
        db_table = "file_info"
        verbose_name = u'文件信息表'
        verbose_name_plural = verbose_name

    def __str__(self) -> str:
        return f"{self.file_name}-{self.file_key}-{self.chunk_num}"

    @property
    def part_name(self):
        return f"{self.file_name}{self.chunk_num}"

    def update(self,**kwargs):
        for k,v in kwargs.items():
            if hasattr(self,k):
                setattr(self,k,v)

class DownLoadRecord(BaseModel):
    class Meta:
        db_table = "download_record"
        verbose_name = u'下载记录表'
        verbose_name_plural = verbose_name

    down_code = models.CharField(max_length=255,verbose_name="文件下载码",null=True)
    down_finish = models.BooleanField(verbose_name="是否下载完成",default=False)
    down_file = models.ForeignKey(to=FileInfo,verbose_name="下载的文件",on_delete=models.CASCADE,null=True)


class test(BaseModel):

    value =  models.CharField(max_length=128,verbose_name="文件名")

    class Meta:
        db_table = "test"
        verbose_name = u'test'
        verbose_name_plural = verbose_name

