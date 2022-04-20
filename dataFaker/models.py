import os
from django.db import models
from core.base import BaseModel
from core import settings
# Create your models here.


def file_directory_path(instance):
    target_path = 'faker/{record_key}'.format(instance.record_key)
    if os.path.exists(os.path.join(settings.MEDIA_ROOT,target_path)):
        os.remove(os.path.join(settings.MEDIA_ROOT,target_path))
    return target_path

class DataFakerRecordInfo(BaseModel):
    # 上传时第一步会发送一个POST请求会生成一个唯一KEY
    record_key = models.CharField(max_length=255,verbose_name="记录唯一标识",null=False,db_index=True)
    is_delete = models.BooleanField(verbose_name="是否删除",default=False)
    expire_time = models.DateTimeField(verbose_name="过期时间",null=False)
    file = models.FileField(max_length=255, upload_to=file_directory_path,null=True)
    download_code = models.CharField(max_length=255,verbose_name="文件下载码",null=True)
    is_finish = models.BooleanField(verbose_name="数据是否已经生成完成",default=False)

    class Meta:
        db_table = "faker_record"
        verbose_name = u'假数据生成记录表'
        verbose_name_plural = verbose_name

    def __str__(self) -> str:
        return f"{self.record_key}"

    def update(self,**kwargs):
        for k,v in kwargs.items():
            if hasattr(self,k):
                setattr(self,k,v)
