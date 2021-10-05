'''
Description: 
email: 359066432@qq.com
Author: lhj
software: vscode
Date: 2021-10-04 01:55:10
platform: windows 10
LastEditors: lhj
LastEditTime: 2021-10-04 02:12:15
'''
from django.db import models
from core.base import BaseModel
# Create your models here.

class DrugWords(BaseModel):
    class Meta:
        db_table="drug_words"
        verbose_name = "毒鸡汤"
        verbose_name_plural = "毒鸡汤"

    content = models.TextField(verbose_name="内容",null=False,blank=False)
    is_show = models.BooleanField(verbose_name="是否展示",default=True,null=False)
    is_custom = models.BooleanField(verbose_name="是否为用户自定义",default=False,null=False)