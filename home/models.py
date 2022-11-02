'''
Description: 
email: 359066432@qq.com
Author: lhj
software: vscode
Date: 2021-10-04 18:46:56
platform: windows 10
LastEditors: lhj
LastEditTime: 2021-10-05 18:10:09
'''

from django.db import models
from core.base import BaseModel
from django.contrib.auth.models import User

class UpdateLog(BaseModel):
    class Meta:
        db_table="site_update_log"
        verbose_name = "更新日志"
        verbose_name_plural = "更新日志"

    update_content = models.TextField(verbose_name="更新内容",null=False,blank=False)
    is_finish = models.BooleanField(verbose_name="完成",default=True,null=False)
    # is_custom = models.BooleanField(verbose_name="是否为用户自定义",default=False,null=False)
    author = models.ForeignKey(User,on_delete=models.CASCADE,related_name="update_author")
    finish_time = models.DateTimeField(verbose_name='完成时间')


class HomePictures(BaseModel):
    class Meta:
        db_table = "site_back_pic"
        verbose_name = "网站主页照片显示"
        verbose_name_plural = "网站主页照片显示"

    path = models.CharField(max_length=128, null=False,
                            verbose_name="图片路径", help_text="主页图片路径")
    is_able = models.BooleanField(
        default=True, help_text="是否启用", verbose_name="是否启用")


class FriendsLink(BaseModel):
    class Meta:
        db_table = "site_friends_links"
        verbose_name = "伙伴链接"
        verbose_name_plural = "伙伴连接"

    site = models.CharField(
        max_length=256, help_text="url 链接", verbose_name="url链接")

    title = models.CharField(max_length=64, verbose_name="链接名称")

    intro = models.CharField(max_length=128, verbose_name="一句话介绍")

    # cover = models.ImageField(
    #     upload_to='blog/friendsLinkCover/%Y%m%d/', blank=True, verbose_name="链接封面")

    cover = models.CharField(
        max_length=256, blank=True, verbose_name="链接封面")

    author = models.CharField(
        max_length=64, verbose_name="作者", default="不愿意透露姓名的小伙")
    is_show = models.BooleanField(verbose_name="允许显示", default=True)


class BackGroundMusic(BaseModel):
    class Meta:
        db_table = "site_back_music"
        verbose_name = "背景音乐"
        verbose_name_plural = "背景音乐合集"

    musicId = models.CharField(
        max_length=64, verbose_name="音乐ID", null=False, blank=False, unique=True)

    title = models.CharField(
        max_length=64, verbose_name="歌名", default="随机播放的音乐")

    name = models.CharField(
        max_length=64, verbose_name="作者", default="UNKNOWN")

    type = models.CharField(
        max_length=64, verbose_name="类型", default="UNKNOWN")

    url = models.CharField(
        max_length=128, verbose_name="音乐源", null=False, blank=False)

    avatar = models.CharField(max_length=128, verbose_name="缩略图保存的本地路径")

    is_user = models.BooleanField(default=True, verbose_name="是否允许使用")

    
class SiteComments(BaseModel):
    
    class Meta:
        db_table = "site_comments"
        verbose_name = "网站留言"
        verbose_name_plural = "网站留言"
        ordering = ['id']


    body = models.TextField(help_text="评论内容", verbose_name="评论内容", null=True)

    likes = models.IntegerField(
        help_text="评论点赞数", verbose_name="评论点赞数", default=0)

    qq = models.CharField(max_length=64, help_text="留言人QQ",
                        verbose_name="留言人qq", null=True)

    email = models.EmailField(
        help_text="留言人邮箱", verbose_name="留言人邮箱", null=True)

    is_valid = models.BooleanField(
        help_text="是否合法(显示)", verbose_name="是否合法(显示)", default=True)

    name = models.CharField(max_length=64, help_text="留言用户姓名",
                            verbose_name="留言用户姓名", default="游客")

    ip = models.GenericIPAddressField(
        verbose_name="调用的IP地址", null=True, blank=True)

    loc_province = models.CharField(
        max_length=256, verbose_name="调用地址(省份)", null=True)
    loc_country = models.CharField(
        max_length=256, verbose_name="调用地址(国家)", null=True)
    loc_city = models.CharField(
        max_length=256, verbose_name="调用地址(城市)", null=True)

    replay_to =models.ForeignKey("self",on_delete=models.CASCADE,related_name="sitecomment_replay_to",null=True,blank=True)
