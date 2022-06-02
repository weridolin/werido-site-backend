'''
Description: 
email: 359066432@qq.com
Author: lhj
software: vscode
Date: 2021-09-11 15:01:27
platform: windows 10
LastEditors: lhj
LastEditTime: 2021-11-18 00:37:56
'''
from django.contrib import admin
from django.db import models
from .models import UserProfile,UserRoleMemberShip
# Register your models here.

## 多对多中间模型 admin显示
# @https://docs.djangoproject.com/zh-hans/3.2/ref/contrib/admin/#modeladmin-objects
# class UserRoleMemberShipInline(admin.TabularInline):
#     model =UserRoleMemberShip
#     extra =1


@admin.register(UserProfile)
class AdminRole(admin.ModelAdmin):
    # inlines = (UserRoleMemberShipInline,)
    list_display=UserProfile.get_db_fields()+["user","show_roles"]

    def show_roles(self,obj):
        role_list = []
        for g in obj.roles.all():
            role_list.append(g.name)
        return ','.join(role_list)

    show_roles.short_description = "角色" 
