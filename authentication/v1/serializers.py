'''
Description: 
email: 359066432@qq.com
Author: lhj
software: vscode
Date: 2021-09-11 15:17:26
platform: windows 10
LastEditors: lhj
LastEditTime: 2021-10-31 12:22:49
'''
from pyexpat import model
from django.contrib.auth.models import User
from authentication.models import UserProfile,ThirdOauthInfo
from core.base import BaseSerializer
from rest_framework import serializers
import uuid

class UserSerializer(BaseSerializer):
    last_login = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    date_joined = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    class Meta:
        model = User
        fields =[
            "id",
            "last_login",
            "first_name",
            "username",
            "last_name",
            "email",
            "is_superuser",
            "date_joined"]


    def update(self, instance, validated_data):
        """"""
        return super().update(instance, validated_data)


class UserProfileSerializer(BaseSerializer):
    """"""
    user = UserSerializer() # 密码字段等都不显示，所以要自定义serializer

    class Meta:
        model = UserProfile
        fields = "__all__"
        depth = 1 # 指定遍历的深度 .默认外键只会序列化到id，而非具体的model

    def update(self, instance, validated_data):
        """this is update"""
        return super().update(instance, validated_data)

    
    def create(self, validated_data):
        """this is created"""
        return super().create(validated_data)


class OauthInfoSerializer(BaseSerializer):
    class Meta:
        model=ThirdOauthInfo
        fields = "__all__"
        depth = 1


from rest_framework_simplejwt.serializers import TokenObtainPairSerializer,TokenRefreshSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rbac.permission import get_user_perms
from django_redis import get_redis_connection
from redis.client import Redis
from utils.redis_keys import UserPermission
import json
from core import settings
import datetime

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    # jwt加入用户的权限和角色
    @classmethod
    def get_token(cls, user):
        token =  super().get_token(user)
        _uuid = str(uuid.uuid4())
        # 增加增定义的字段
        roles,groups,role_perms = get_user_perms(user=user)
        token["uuid"] = _uuid
        token["flag"] = "werido-site"
        token["name"] = user.username
        token["groups"] = [(group.group_name,group.id)for group in groups]
        token["roles"] = [(role.role_name,role.id)for role in roles]
        # token["perms"] = perms
    
            # 把权限缓存到redis.
        conn:Redis = get_redis_connection("default") # return redis client:<redis.client.Redis>
        
        conn.set(
            UserPermission.permission_key(user,_uuid),
            json.dumps(role_perms,ensure_ascii=False),
            ex=settings.SIMPLE_JWT.get("ACCESS_TOKEN_LIFETIME")+datetime.timedelta(minutes=2)) # 比TOKEN的过期时间多加2分分钟
            
        return token


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class=CustomTokenObtainPairSerializer       


# class UserSerializer