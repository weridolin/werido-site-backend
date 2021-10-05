'''
Description: 
email: 359066432@qq.com
Author: lhj
software: vscode
Date: 2021-10-02 23:34:02
platform: windows 10
LastEditors: lhj
LastEditTime: 2021-10-03 02:19:01
'''
from django.dispatch import Signal
from django.dispatch import receiver
from articles.models import Article
from django.db.models.signals import post_save
import datetime
update_pre_and_next_signal=Signal()

@receiver(update_pre_and_next_signal,sender=Article,dispatch_uid="update_pre_and_next")
def update_pre_and_next(sender,instance,created=False,**kwargs):
    # print(">>",instance.pre.id,instance.id,created,datetime.datetime.now())
    if  created and instance.pre:
        if instance.pre.next is None:
                instance.pre.next = instance
                instance.pre.save()

