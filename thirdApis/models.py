from django.db import models
import datetime
# Create your models here.
from core.base import BaseModel
from django.contrib.auth.models import User
import uuid

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

    run_command = models.TextField(
        null=False, help_text="运行命令", verbose_name="运行命令", default="echo no-command")


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


def get_uuid():
    return str(uuid.uuid4())


### GPT 相关

PLATFORM = (    
    ("chatGPT","chatGPT"),
    ("通义千问","通义千问")
)

class GptConversation(BaseModel):
    class Meta:
        db_table = "gpt_conversation"
        verbose_name = "chatGPT聊天会谈" 
        verbose_name_plural = "chatGPT聊天会谈"

    title = models.CharField(null=False, max_length=128,help_text="会话名称", verbose_name="会话名称")
    uuid = models.UUIDField(help_text="会话ID", verbose_name="会话ID",db_index=True, default=get_uuid,primary_key=True)
    user_id = models.SmallIntegerField(verbose_name="会话创建者", null=False, help_text="会话创建者")
    model = models.CharField(max_length=64, null=False, help_text="模型名称", verbose_name="模型名称")
    description = models.TextField(null=True, help_text="会话描述", verbose_name="会话描述")
    platform = models.CharField(max_length=64, null=False, help_text="平台名称", verbose_name="平台名称",choices=PLATFORM)   
    key = models.CharField(max_length=256, null=False, help_text="当前会话使用的API KEY", verbose_name="API-KEY",default="")    
    deleted = models.BooleanField(help_text="是否删除", verbose_name="是否删除",default=False)

MESSAGE_ROLE = (
    ("system", "system"),
    ("user", "user")
)

STOP_TYPE = (
    ("interrupt", "interrupt"), # 中断 
    ("timeout", "timeout") # 中断
)


class GptMessage(BaseModel):
    class Meta:
        db_table = "gpt_message"
        verbose_name = "GPT聊天消息"
        verbose_name_plural = "GPT聊天消息"

    uuid = models.UUIDField(default=get_uuid,help_text="消息UUID", verbose_name="消息UU会话ID", db_index=True,primary_key=True)
    conversation_id = models.UUIDField(verbose_name="所属会话ID", help_text="所属会话ID", null=False)
    # role = models.CharField(max_length=16,choices=MESSAGE_ROLE, verbose_name="消息发送者角色", help_text="消息发送者角色")
    query_content = models.TextField(verbose_name="消息内容", help_text="消息内容")
    query_content_type = models.CharField(max_length=16, verbose_name="消息类别", help_text="消息类型",default="text")
    reply_content_type = models.CharField(max_length=16, verbose_name="消息类别", help_text="消息类型",default="text")
    parent_message_uuid = models.UUIDField(null=True,help_text="上一条消息UUID,主要记录会话里面的顺序", verbose_name="上一条消息ID")
    children_message_uuid = models.UUIDField(help_text="下一条消息UUID,主要记录会话里面的顺序", null=True,verbose_name="下一条消息ID")
    reply_content = models.TextField(null=True,help_text="回复内容", verbose_name="回复内容",blank=True)
    reply_finish = models.BooleanField(help_text="是否回复完成", verbose_name="是否回复完成",default=False)
    user_id = models.SmallIntegerField(verbose_name="消息发送者", null=False, help_text="消息发送者")
    interrupt = models.BooleanField(help_text="是否半途停止", verbose_name="是否半途停止",default=False)
    interrupt_reason = models.CharField(max_length=128, verbose_name="停止类型", help_text="停止类型",null=True,blank=True)
    websocket_id = models.CharField(max_length=64, verbose_name="websocketID", help_text="该次对话对应的websocketID",default=get_uuid,db_index=True) # 
    has_sended = models.BooleanField(help_text="是否已经发送给客户端", verbose_name="是否已经发送给客户端",default=False)
    error = models.BooleanField(help_text="是否出错", verbose_name="是否出错",default=False)
    error_code = models.CharField(max_length=64, null=True,help_text="错误代码", verbose_name="错误代码",blank=True)
    error_detail = models.CharField(max_length=256,null=True,help_text="错误详情", verbose_name="错误详情",blank=True)