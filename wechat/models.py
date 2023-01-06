from django.db import models

# Create your models here.
from core.base import BaseModel


class WechatMessage(BaseModel):
    class Meta:
        db_table = "wechat_public_count_message"
        verbose_name = "微信公众号消息记录"
        verbose_name_plural = "微信公众号消息记录"

    msg_id = models.BigIntegerField(verbose_name='消息id,64位整型',help_text="消息id,64位整型",unique=True)
    msg_to = models.CharField(
        max_length=256, help_text="开发者微信号", verbose_name="开发者微信号")
    msg_from = models.CharField(
        max_length=256, help_text="发送方帐号(一个OpenID)", verbose_name="发送方帐号(一个OpenID)")
    create_time = models.BigIntegerField(
        help_text="消息创建时间", verbose_name="消息创建时间", null=False)
    msg_type = models.CharField(
        max_length=32, help_text="消息类型(文本:text,图片:image,语音:voice,视频:video,小视频:shortvideo,地理位置:location,链接:link)", verbose_name="消息类型", null=False)

    content = models.TextField(verbose_name='消息内容',help_text="消息内容",null=True)

    msg_data_id = models.CharField(max_length=256,null=True,verbose_name="消息的数据ID",help_text="消息的数据ID(消息如果来自文章时才有)")

    idx = models.IntegerField(verbose_name="多图文时第几篇文章",null=True,help_text="多图文时第几篇文章，从1开始（消息如果来自文章时才有）")

    media_id = models.CharField(max_length=256,null=True,verbose_name="语音/视频消息媒体id，可以调用获取临时素材接口拉取数据",help_text="语音消息媒体id，可以调用获取临时素材接口拉取数据")

    voice_format = models.CharField(max_length=32,null=True,verbose_name="语音格式",help_text="语音格式")

    voice_recognition = models.TextField(verbose_name="语音识别结果",null=True,help_text="语音识别结果(UTF-8编码)")

    thumb_media_id = models.CharField(max_length=256,null=True,verbose_name="视频消息缩略图的媒体id,可以调用多媒体文件下载接口拉取数据。",help_text="视频消息缩略图的媒体id,可以调用多媒体文件下载接口拉取数据。")


    ### link 相关消息
    link_title=models.CharField(max_length=256,verbose_name="链接消息标题",help_text="链接消息标题",null=True)

    link_description=models.TextField(verbose_name="链接消息描述",help_text="链接消息描述",null=True)

    link_url = models.URLField(verbose_name="消息链接url",help_text="消息链接url",null=True)
