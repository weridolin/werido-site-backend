from django.db import models
import datetime
# Create your models here.
from core.base import BaseModel
from django.contrib.auth.models import User

TYPE_ALIAS = {

}

SrcTypes = [
    ("self", "self"),
    ("xl", "xl"),
    ("tx", "tx"),
]


class ShortUrlRecords(BaseModel):
    class Meta:
        db_table = "short_uri_records"
        verbose_name = "短链接记录"
        verbose_name_plural = "短链接记录"
        unique_together = (
            ('type', 'url'),  # 联合唯一
        )
    url = models.URLField(null=False, help_text="url", verbose_name="url")
    short_flag = models.CharField(
        max_length=64, null=True, default="undefined", help_text="短链接", verbose_name="短链接")
    description = models.TextField(
        null=True, help_text="描述", verbose_name="url描述")
    type = models.CharField(max_length=16, verbose_name="类别对应的模型",
                            choices=SrcTypes, default="self", null=False, blank=False)
    expire_time = models.DateTimeField(
        verbose_name="过期时间", null=False, help_text="过期时间")

    def __unicode__(self):
        return self.short_flag

    def __str__(self):
        return self.short_flag


def default_expire_time():
    return datetime.datetime.now()+datetime.timedelta(days=7)


class ApiCollector(BaseModel):

    class Meta:
        db_table = "ac_info_set"
        verbose_name = "各大Api集合"
        verbose_name_plural = "各大Api集合"
        # unique_together = (
        #     ('type','url'),  # 联合唯一
        # )

    platform = models.CharField(
        max_length=64, null=False, default="uncle-lin", help_text="api所属平台", verbose_name="api所属平台")
    is_free = models.BooleanField(
        default=False, null=False, help_text="是否免费", verbose_name="是否免费")
    api_type = models.CharField(
        max_length=64, null=False, default="", help_text="api所属类别", verbose_name="api所属类别")
    api_name = models.CharField(
        max_length=64, null=False, default="unknown", help_text="api名称", verbose_name="api名称")
    api_icon = models.CharField(
        max_length=64, null=False, help_text="api对应的icon", verbose_name="api对应的icon")
    api_url = models.URLField(
        null=False, help_text="api对应的url", default="unknown", verbose_name="api对应的url")
    clicked = models.PositiveIntegerField(
        null=False, default=0, help_text="点击次数", verbose_name="点击次数")
    expire_time = models.DateTimeField(
        verbose_name="过期时间", null=False, help_text="过期时间", default=default_expire_time)
    api_price = models.FloatField(
        null=False, help_text="Api价格", default=0.0, verbose_name="Api价格")
    api_price_unit = models.CharField(
        max_length=64, null=False, help_text="Api价格单位", default=0.0, verbose_name="Api价格单位")

    def __str__(self):
        return self.api_name

    def __repr__(self) -> str:
        return self.api_name


class ApiCollectorSpiderRunRecord(BaseModel):
    class Meta:
        db_table = "ac_spider_run_record"
        verbose_name = "apiSpider执行记录"
        verbose_name_plural = "apiSpider执行记录"

    pid = models.IntegerField(
        null=False, help_text="脚本运行的进程ID", default="unknown", verbose_name="脚本运行的进程ID")
    # pid_path =
    name = models.CharField(null=False, max_length=128,
                            help_text="脚本名称", verbose_name="脚本名称")
    log_path = models.CharField(
        max_length=128, null=False, help_text="脚本运行的日志地址", verbose_name="脚本运行的日志地址")
    finish_time = models.DateTimeField(
        verbose_name="完成时间", null=False, help_text="完成时间", default=datetime.datetime.now)
    result = models.SmallIntegerField(
        default=2, help_text="脚本运行结果,成功为0,异常为1,正在运行为2", verbose_name="脚本运行结果,成功为0,异常为1,正在运行为2")
    invoker = models.ForeignKey(
        User, on_delete=models.DO_NOTHING, verbose_name="调用者", null=False, help_text="调用者")
    unique_flag = models.CharField(
        max_length=128, null=False, help_text="脚本运行记录唯一标识", verbose_name="脚本运行记录唯一标识")
    err_reason = models.TextField(
        null=True, help_text="错误信息", verbose_name="错误信息")
    
    run_command = models.TextField(null=False, help_text="运行命令", verbose_name="运行命令",default="echo no-command")

class ApiCollectorSpiderResourceModel(BaseModel):
    class Meta:
        db_table = "ac_spider_resource"
        verbose_name = "apiSpider可用资源"
        verbose_name_plural = "apiSpider可用资源"

    name = models.CharField(null=False, max_length=128,
                            help_text="脚本名称", verbose_name="脚本名称", unique=True)
    script_path = models.CharField(
        max_length=128, null=False, help_text="脚本储存路径", verbose_name="脚本储存路径")
    last_run_time = models.DateTimeField(
        verbose_name="上次运行时间", null=True, help_text="上次运行时间")
    run_count = models.PositiveIntegerField(
        verbose_name="运行次数", null=False, help_text="运行次数", default=0)
    is_forbidden = models.BooleanField(
        null=False, help_text="该脚本是否被禁用", verbose_name="该脚本是否被禁用", default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                            verbose_name="创建者", null=False, help_text="创建者")
    run_command = models.CharField(
        max_length=256, null=True, help_text="运行指令", verbose_name="运行指令")
    description = models.TextField(
        null=True, help_text="脚本描述", verbose_name="脚本描述")
