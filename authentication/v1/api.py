'''
Description: 
email: 359066432@qq.com
Author: lhj
software: vscode
Date: 2021-09-11 14:46:52
platform: windows 10
LastEditors: lhj
LastEditTime: 2021-11-28 23:05:04
'''
import json
from redis import client
import requests
from rest_framework import views, viewsets, status
from rest_framework.response import Response
from django.http import HttpResponseForbidden,HttpResponseNotFound,HttpResponseBadRequest
from rest_framework import permissions
from django.contrib.auth.models import Permission, User
from authentication.models import UserProfile
from rest_framework.authentication import  SessionAuthentication, TokenAuthentication, get_authorization_header
from authentication.v1.serializers import UserProfileSerializer
from authentication.v1.singals import created_done
from rest_framework.decorators import action
from rest_framework_simplejwt.authentication import JWTAuthentication
from utils.http_ import HTTPResponse


class IsUserAlreadyExistPermission(permissions.BasePermission):
    ## TODO 改成用serializer去校验
    message = ''
    def has_permission(self, request, view):
        # print(request.user.is_authenticated)
        if request.method == "POST":
            # 此时跳过验证， request user = None!
            username = request.data.get("username", None)
            email = request.data.get("email", None)
            telephone = request.data.get("telephone", None)
            if username:
                if User.objects.filter(username=username).exists():
                    IsUserAlreadyExistPermission.message = f"user:{username} is already exist"
                    return False
            if email:
                if User.objects.filter(email=email).exists(): # TODO 改成唯一
                    # IsUserAlreadyExistPermission.message = f"email:{email} is already exist"
                    return True
            if telephone:
                if UserProfile.objects.filter(telephone=telephone).exists():
                    IsUserAlreadyExistPermission.message = f"telephone:{telephone} is already exist"
                    return False
            IsUserAlreadyExistPermission.message = ""
            return True
        else:
            return super().has_permission(request, view)


from rest_framework_simplejwt.exceptions import InvalidToken

class ProfileApisAuthentication(JWTAuthentication):

    def authenticate(self, request):
        if request.method == "POST":# 注册方法统一为管理员用户的权限进行注册
            user = User.objects.get(username="werido")
            return (user, None) # return NONE才会引发 401 @https://www.django-rest-framework.org/api-guide/authentication/
        else:
            return super().authenticate(request)
    
from rest_framework.throttling import UserRateThrottle,AnonRateThrottle

class UserProfileApis(viewsets.ModelViewSet):
    """
    

    """
    authentication_classes=[ProfileApisAuthentication]
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    
    def get_permissions(self):
        if self.action in ['register'] :
            permission_classes = [IsUserAlreadyExistPermission,permissions.AllowAny]
        elif self.action in ['unregister'] :
            permission_classes = [permissions.IsAuthenticated]
        elif self.action in ['search']:
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]

    @action(methods=["DELETE"],detail=False)     # 会先校验 permission,再检验method是否合法
    def unregister(self, request):
        """删除用户 only admin"""
        if not request.user.is_superuser:
            return HttpResponseForbidden("ONLY SUPER USER CAN OPERATE!")
        # todo admin 判断
        return Response(
            "delete",
            status=status.HTTP_200_OK
        )

    # 一天只允许注册  100 个用户
    @action(methods=["POST"],detail=False,throttle_classes=[AnonRateThrottle])
    def register(self, request, **kwargs):
        """ 注册用户 """
        # todo错误回滚
        username = request.data.get("username")
        email = request.data.get("email")
        password = request.data.get("password")
        new_user = User.objects.create(
            username=username, email=email)
        new_user.set_password(password) # 密码不能明文保存
        new_user.save()
        count = User.objects.count() 
        created_done.send(sender=new_user.__class__, created=True,
                        instance=new_user, number=count+1,**filter_profie(request.data))          
        # from core.celery import send_welcome_mail
        # send_welcome_mail.delay(receiver=email)
        return HTTPResponse(
            code=status.HTTP_200_OK,message=f"created user:{username} success!",app_code="auth"
        )


    @action(methods=["PUT","GET"],detail=False,throttle_classes=[UserRateThrottle])
    def profile(self, request):
        """ 修改用户信息  """
        if not request.user.is_authenticated:
            return HTTPResponse(code=-1,status=status.HTTP_401_UNAUTHORIZED,app_code="auth",message="please login first")
        try: 
            info = UserProfile.objects.get(user_id = request.user.id)
            if request.method=="PUT":
                # 修改用户信息
                for key,value in request.data.items():
                    if hasattr(info,key):
                        setattr(info,key,value)
                        print(key,value)
                info.save()
                return HTTPResponse(message="update success",status=status.HTTP_200_OK,app_code="auth")
            elif request.method =="GET":
                serializer_data = UserProfileSerializer(info)
                return HTTPResponse(data=serializer_data.data,app_code="auth")  
        except UserProfile.DoesNotExist:
            return HttpResponseNotFound(f"can not find user :{request.user.username} profile!")

    @action(methods=["GET"],detail=False)
    def search(self,request):
        username = request.query_params.get("username",None)
        email = request.query_params.get("email",None)
        try:
            if username and username!='':
                user = User.objects.get(username=username)
            elif email and email!='':
                user = User.objects.get(email=email) 
            profile_info = UserProfile.objects.get(user_id = user.id)
            serializer_data = UserProfileSerializer(profile_info)
            payload = {"data":serializer_data.data,"code":200} 
            return Response(data=payload,status=status.HTTP_200_OK) 
        except (User.DoesNotExist,UserProfile.DoesNotExist ):
            payload = {"data":[],"code":404}
            return Response(data=payload,status=status.HTTP_404_NOT_FOUND)         
        

def filter_profie(info:dict):
    result = {}
    for key in UserProfile.get_db_fields():
        if  key in info.keys():
            result.update({key:info.get(key)})
    return result

from django.contrib.auth import login,logout,authenticate
from .serializers import CustomTokenObtainPairSerializer
from django_redis import get_redis_connection
from redis.client import Redis
import json
import time

class AuthApis(viewsets.ModelViewSet):

    authentication_classes=[JWTAuthentication]
    serializer_class = UserProfileSerializer

    def get_permissions(self):
        if self.action in ['login'] :
            permission_classes = []
        elif self.action in ['logout'] :
            permission_classes = []
        else:
            print("undefined",self.action)
            permission_classes = []
        return [permission() for permission in permission_classes]
    
    @action(methods=["POST"],detail=False,url_path="login")
    def login(self,request):
        username = request.data.get("username",None)
        password = request.data.get("password",None)
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            try:
                user_profile = UserProfile.objects.get(user_id = user.id)
            # permissions = get_permission(user_profile=user_profile)
            except UserProfile.DoesNotExist:
                user_profile = None

            # 将permission缓存到redis
            # conn:Redis = get_redis_connection("default") # return redis client:<redis.client.Redis>
            # conn.set(UserBriefInfo.from_user(user).cache_permission_key,
            #     json.dumps(permissions,ensure_ascii=False))
            
            # refresh_token = RefreshToken.for_user(user) # 默认的token
            refresh_token = CustomTokenObtainPairSerializer.get_token(user=user) # 添加了自定义的token
            data= {
                "access_token":str(refresh_token.access_token),
                "refresh_token":str(refresh_token),
                # "permissions_dict":permissions,
                "profile":UserProfileSerializer(instance=user_profile).data if user_profile else None
            }
            return HTTPResponse(
                data=data,
                code=0,
                app_code="auth",
                status=status.HTTP_200_OK
            )
        else:
            return HTTPResponse(
                code=-1,
                status=status.HTTP_403_FORBIDDEN,
                message="账户名或密码错误!",
                app_code="auth"
            )
        
        

    @action(methods=["POST"],detail=False)
    def logout(self,request):
        # _user = request.user
        _ = logout(request=request) # logout之后request user会被清空
        # 清除缓存
        # conn:Redis = get_redis_connection("default") # return redis client:<redis.client.Redis>
        # conn.delete(UserBriefInfo.from_user(_user).cache_permission_key.encode())
        return HTTPResponse(
            status=status.HTTP_200_OK,
            code=0,
            app_code="auth",
            message="logout success"
        )


