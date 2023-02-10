from django.db import models
# from core.base import BaseModel
# Create your models here.


class BaseModel(models.Model):
    created = models.DateField(
        auto_now_add=True, verbose_name='创建时间', db_index=True)
    updated = models.DateField(
        auto_now=True, verbose_name='修改时间', db_index=True)

    class Meta:
        app_label = 'Covid'
        managed = False
        abstract = True


class Country(BaseModel):
    class Meta:
        db_table = "covid19_country_data"
        verbose_name = "国家疫情统计"
        verbose_name_plural = "省份疫情统计"

    # country_code= models.CharField(verbose_name="国家对应的高德地图里面的编码",max_length=32,unique=True,null=False,blank=False,help_text="国家对应的高德地图里面的编码")
    country_name_cn = models.CharField(
        verbose_name="国家名称中文", max_length=32, unique=True, null=False, blank=False, help_text="国家名称中文")
    country_name_en = models.CharField(
        verbose_name="国家名称英文", max_length=32, unique=True, null=False, blank=False, help_text="国家名称英文")

    # current_confirmed_count = models.IntegerField(
    #     verbose_name="新增确诊人数",null=False,blank=False,help_text="新增确诊人数",default=0)

    confirmed_count = models.IntegerField(
        verbose_name="确诊总人数", null=False, blank=False, help_text="确诊总人数", default=0)
    # current_confirmed_count_no_symptom = models.IntegerField(
    #     verbose_name="新增无症状确诊人数",null=False,blank=False,help_text="新增无症状确诊人数",default=0)
    cured_count = models.IntegerField(
        verbose_name="治愈人数", null=False, blank=False, help_text="治愈人数", default=0)
    dead_count = models.IntegerField(
        verbose_name="死亡人数", null=False, blank=False, help_text="死亡人数", default=0)


class Province(BaseModel):

    class Meta:
        db_table = "covid19_province_data"
        verbose_name = "省份疫情统计"
        verbose_name_plural = "省份疫情统计"

    province_code = models.CharField(verbose_name="省份对应的高德地图里面的编码", max_length=32,
                                     unique=True, null=False, blank=False, help_text="省份对应的高德地图里面的编码")

    province_name = models.CharField(
        verbose_name="省份名称", max_length=32, unique=True, null=False, blank=False, help_text="省份名称")

    current_confirmed_count = models.IntegerField(
        verbose_name="新增确诊人数", null=False, blank=False, help_text="新增确诊人数", default=0)

    confirmed_count = models.IntegerField(
        verbose_name="确诊总人数", null=False, blank=False, help_text="确诊总人数", default=0)
    current_confirmed_count_no_symptom = models.IntegerField(
        verbose_name="新增无症状确诊人数", null=False, blank=False, help_text="新增无症状确诊人数", default=0)
    cured_count = models.IntegerField(
        verbose_name="治愈人数", null=False, blank=False, help_text="治愈人数", default=0)
    dead_count = models.IntegerField(
        verbose_name="死亡人数", null=False, blank=False, help_text="死亡人数", default=0)


class City(BaseModel):
    class Meta:
        db_table = "covid19_city_data"
        verbose_name = "城市疫情统计"
        verbose_name_plural = "城市疫情统计"
        # unique_together = ('city_name','created')

    city_code = models.CharField(verbose_name="城市对应的高德地图里面的编码", max_length=32,
                                null=False, blank=False, help_text="城市对应的高德地图里面的编码")

    city_name = models.CharField(verbose_name="城市名称", max_length=64,
                                null=False, blank=False, help_text="城市名称")

    city_name_en = models.CharField(
        verbose_name="城市名称英文", max_length=64, null=True, blank=False, help_text="城市名称英文")

    province_code = models.CharField(verbose_name="省份对应的高德地图里面的编码", max_length=32,
                                    null=False, blank=False, help_text="省份对应的高德地图里面的编码")

    province_name = models.CharField(
        verbose_name="省份名称", max_length=64, null=False, blank=False, help_text="省份名称")
    province_name_en = models.CharField(
        verbose_name="省份名称英文", max_length=64, null=True, blank=False, help_text="省份名称英文")

    # country_code= models.CharField(verbose_name="国家对应的高德地图里面的编码",max_length=32,unique=True,null=False,blank=False,help_text="国家对应的高德地图里面的编码")
    country_name_cn = models.CharField(
        verbose_name="国家名称中文", max_length=64,  null=False, blank=False, help_text="国家名称中文")

    country_name_en = models.CharField(
        verbose_name="国家名称英文", max_length=64,  null=True, blank=False, help_text="国家名称英文")

    current_confirmed_count = models.IntegerField(
        verbose_name="新增确诊人数", null=False, blank=False, help_text="新增确诊人数", default=0)

    confirmed_count = models.IntegerField(
        verbose_name="确诊总人数", null=False, blank=False, help_text="确诊总人数", default=0)
    current_confirmed_count_no_symptom = models.IntegerField(
        verbose_name="新增无症状确诊人数", null=False, blank=False, help_text="新增无症状确诊人数", default=0)
    cured_count = models.IntegerField(
        verbose_name="治愈人数", null=False, blank=False, help_text="治愈人数", default=0)
    dead_count = models.IntegerField(
        verbose_name="死亡人数", null=False, blank=False, help_text="死亡人数", default=0)


class Policy(BaseModel):
    class Meta:
        db_table = "covid19_policy"
        verbose_name = "防疫政策"
        verbose_name_plural = "防疫政策"

    title = models.CharField(
        verbose_name="政策名称", max_length=256, null=False, blank=False, help_text="政策名称")
    loc = models.CharField(verbose_name="发布地", max_length=256,
                           null=False, blank=False, help_text="发布地")
    src = models.CharField(verbose_name="消息源链接", max_length=256,
                           null=False, blank=False, help_text="消息源链接")


class News(BaseModel):
    class Meta:
        db_table = "covid19_news"
        verbose_name = "疫情新闻"
        verbose_name_plural = "疫情新闻"

    title = models.CharField(
        verbose_name="政策名称", max_length=256, null=False, blank=False, help_text="政策名称")
    loc = models.CharField(verbose_name="发布地", max_length=256,
                           null=False, blank=False, help_text="发布地")
    src = models.CharField(verbose_name="消息源", max_length=256,
                           null=False, blank=False, help_text="消息源")
    url = models.CharField(verbose_name="消息源链接", max_length=256,
                           null=False, blank=False, help_text="消息源链接")
    type = models.CharField(
        verbose_name="新闻类型", max_length=32, null=False, blank=False, help_text="新闻类型")
    summary = models.TextField(
        verbose_name="消息摘要",null=True, help_text="消息摘要"
    )