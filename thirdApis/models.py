from email.policy import default
from django.db import models
import datetime
# Create your models here.
from core.base import BaseModel


SrcTypes = [
    ("self","self"),
    ("xl","xl"),    
    ("tx","tx"),   
]
class ShortUrlRecords(BaseModel):
    class Meta:
        db_table = "short_uri_records"
        verbose_name = "短链接记录"
        verbose_name_plural = "短链接记录"
        unique_together = (
            ('type','url'),  # 联合唯一
        )
    url = models.URLField(null=False,help_text="url", verbose_name="url")
    short_flag = models.CharField(max_length=64,null=True,default="undefined",help_text="短链接",verbose_name="短链接")
    description = models.TextField(null=True, help_text="描述", verbose_name="url描述")
    type = models.CharField(max_length=16, verbose_name="类别对应的模型",
                            choices=SrcTypes, default="self", null=False, blank=False)
    expire_time = models.DateTimeField(verbose_name="过期时间",null=False,help_text="过期时间")

    def __unicode__(self):
        return self.short_flag

    def __str__(self):
        return self.short_flag




class ApiCollector(BaseModel):

    class Meta:
        db_table = "api_collector"
        verbose_name = "各大Api集合"
        verbose_name_plural = "各大Api集合"
        # unique_together = (
        #     ('type','url'),  # 联合唯一
        # )    
    
    platform = models.CharField(max_length=64,null=False,default="uncle-lin",help_text="api所属平台",verbose_name="api所属平台")
    is_free = models.BooleanField(default=False,null=False,help_text="是否免费",verbose_name="是否免费")
    api_type = models.CharField(max_length=64,null=False,default="",help_text="api所属类别",verbose_name="api所属类别")
    api_name = models.CharField(max_length=64,null=False,default = "unknown",help_text="api名称",verbose_name="api名称")
    api_icon = models.CharField(max_length=64,null=False,help_text="api对应的icon",verbose_name="api对应的icon")
    api_url = models.URLField(null=False,help_text="api对应的url",default="unknown" ,verbose_name="api对应的url")
    clicked = models.PositiveIntegerField(null=False,default=0,help_text="点击次数",verbose_name="点击次数")
    expire_time = models.DateTimeField(verbose_name="过期时间",null=False,help_text="过期时间",default=datetime.datetime.now()+datetime.timedelta(days=7))
    api_price = models.FloatField(null=False,help_text="Api价格",default=0.0,verbose_name="Api价格")
    api_price_unit = models.CharField(max_length=64,null=False,help_text="Api价格单位",default=0.0,verbose_name="Api价格单位")

    def __str__(self):
        return self.api_name

    def __repr__(self) -> str:
        return self.api_name


class ApiCollectorSpiderRunRecord(BaseModel):
    class Meta:
        db_table = "ac_spider_run_record"
        verbose_name = "apiSpider执行记录"
        verbose_name_plural = "apiSpider执行记录"
    
    pid = models.SmallIntegerField(null=False,help_text="脚本运行的进程ID",default="unknown",verbose_name="脚本运行的进程ID")
    # pid_path = 
    log_path = models.CharField(max_length=128,null=False,help_text="脚本运行的日志地址",verbose_name="脚本运行的日志地址")
    finish_time = models.DateTimeField(verbose_name="完成时间",null=False,help_text="完成时间",default = datetime.datetime.now())
    result = models.SmallIntegerField(default=2,help_text="脚本运行结果,成功为0,异常为1,正在运行为2",verbose_name="脚本运行结果,成功为0,异常为1,正在运行为2")