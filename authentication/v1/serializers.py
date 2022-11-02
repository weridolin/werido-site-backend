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

class UserSerializer(BaseSerializer):
    last_login = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    # updated = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    class Meta:
        model = User
        fields =[
            "last_login",
            "first_name",
            "username",
            "last_name",
            "email"]


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

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token =  super().get_token(user)

        # 增加增定义的字段
        token["flag"]="werido-site"
        roles= []
        # for role in user.profile.roles.all():
        #     roles.append(role.name)
        token["name"] = user.username
        token["roles"] =roles   
        return token


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class=CustomTokenObtainPairSerializer       