from django.db import models
from core.base import BaseModel
# Create your models here.

class Country(BaseModel):

    class Meta:
        __tablename__="covid_country_data"


    country_code= models.CharField(verbose_name="国家对应的高德地图里面的编码",max_length=32,unique=True,null=False,blank=False,help_text="国家对应的高德地图里面的编码")
    country_code_cn= models.CharField(verbose_name="国家名称中文",max_length=32,unique=True,null=False,blank=False,help_text="国家名称中文")
    country_code_en= models.CharField(verbose_name="国家名称英文",max_length=32,unique=True,null=False,blank=False,help_text="国家名称英文")

    current_confirmed_count = models.IntegerField(
        verbose_name="新增确诊人数",null=False,blank=False,help_text="新增确诊人数",default=0)

    confirmed_count = models.IntegerField(
        verbose_name="确诊总人数",null=False,blank=False,help_text="确诊总人数",default=0)
    confirmed_count2 = models.IntegerField(
        verbose_name="无症状确诊人数",null=False,blank=False,help_text="无症状确诊人数",default=0)
    cured_count = models.IntegerField(
        verbose_name="治愈人数",null=False,blank=False,help_text="治愈人数",default=0)
    dead_count = models.IntegerField(
        verbose_name="死亡人数",null=False,blank=False,help_text="死亡人数",default=0)


class Province(BaseModel):
    class Meta:
        __tablename__="covid_province_data"

    country_code= models.CharField(verbose_name="省份对应的高德地图里面的编码",max_length=32,unique=True,null=False,blank=False,help_text="省份对应的高德地图里面的编码")


    current_confirmed_count = models.IntegerField(
        verbose_name="新增确诊人数",null=False,blank=False,help_text="新增确诊人数",default=0)

    confirmed_count = models.IntegerField(
        verbose_name="确诊总人数",null=False,blank=False,help_text="确诊总人数",default=0)
    confirmed_count2 = models.IntegerField(
        verbose_name="无症状确诊人数",null=False,blank=False,help_text="无症状确诊人数",default=0)
    cured_count = models.IntegerField(
        verbose_name="治愈人数",null=False,blank=False,help_text="治愈人数",default=0)
    dead_count = models.IntegerField(
        verbose_name="死亡人数",null=False,blank=False,help_text="死亡人数",default=0)


class City(BaseModel):
    class Meta:
        __tablename__="covid_city_data"

    country_code= models.CharField(verbose_name="城市对应的高德地图里面的编码",max_length=32,unique=True,null=False,blank=False,help_text="城市对应的高德地图里面的编码")

    current_confirmed_count = models.IntegerField(
        verbose_name="新增确诊人数",null=False,blank=False,help_text="新增确诊人数",default=0)

    confirmed_count = models.IntegerField(
        verbose_name="确诊总人数",null=False,blank=False,help_text="确诊总人数",default=0)
    confirmed_count2 = models.IntegerField(
        verbose_name="无症状确诊人数",null=False,blank=False,help_text="无症状确诊人数",default=0)
    cured_count = models.IntegerField(
        verbose_name="治愈人数",null=False,blank=False,help_text="治愈人数",default=0)
    dead_count = models.IntegerField(
        verbose_name="死亡人数",null=False,blank=False,help_text="死亡人数",default=0)


class Policy(BaseModel):
    class Meta:
        __tablename__="covid_policy"

    
    title =  models.CharField(verbose_name="政策名称",max_length=256,null=False,blank=False,help_text="政策名称")   
    loc =  models.CharField(verbose_name="发布地",max_length=256,null=False,blank=False,help_text="发布地")
    src =  models.CharField(verbose_name="消息源链接",max_length=256,null=False,blank=False,help_text="消息源链接")



class News(BaseModel):
    class Meta:
        __tablename__="covid_news"

    
    title =  models.CharField(verbose_name="政策名称",max_length=256,null=False,blank=False,help_text="政策名称")   
    loc =  models.CharField(verbose_name="发布地",max_length=256,null=False,blank=False,help_text="发布地")
    src =  models.CharField(verbose_name="消息源",max_length=256,null=False,blank=False,help_text="消息源")
    url = models.CharField(verbose_name="消息源链接",max_length=256,null=False,blank=False,help_text="消息源链接")
    type = models.CharField(verbose_name="新闻类型",max_length=32,null=False,blank=False,help_text="新闻类型")


    