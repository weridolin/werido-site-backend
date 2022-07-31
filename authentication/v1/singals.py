'''
Description: 
email: 359066432@qq.com
Author: lhj
software: vscode
Date: 2021-09-12 09:03:10
platform: windows 10
LastEditors: lhj
LastEditTime: 2021-11-29 00:30:29
'''

from django.db.models import signals
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from authentication.models import UserProfile,Role
# from rbac.models import Role
from django.dispatch import Signal

created_done = Signal()
from core.celery import send_welcome_mail

#django 的signal是同步执行，如果耗时操作（发送邮件或者email,不建议用信号来处理）
@receiver(created_done,sender=User,dispatch_uid="create-profile")
def created_user_profile(sender,instance,created=False,number=10,**kwargs):
    if created:
        new = UserProfile.objects.create(user=instance)
        try:
            default_role  = Role.objects.get(name="guest")
            new.roles.add(default_role)
        except Role.DoesNotExist:
            pass
        new.save()
        if instance.email:
            send_welcome_mail.delay(receiver=instance.email,number=number,**kwargs)
            