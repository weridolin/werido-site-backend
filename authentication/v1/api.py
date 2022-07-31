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
from ctypes.wintypes import HHOOK
import json
from django.apps import AppConfig
from redis import client
import requests
from rest_framework import views, viewsets, status
from rest_framework.response import Response
from django.http import HttpResponseForbidden,HttpResponseNotFound,HttpResponseBadRequest
from rest_framework import permissions
from django.contrib.auth.models import Permission, User
from authentication.models import UserProfile,ThirdOauthInfo
from rest_framework.authentication import  SessionAuthentication, TokenAuthentication, get_authorization_header
from authentication.v1.serializers import UserProfileSerializer,OauthInfoSerializer
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
from .serializers import CustomTokenObtainPairSerializer, UserSerializer
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

from urllib.parse import urlencode
from urllib import parse
from utils.http_ import HTTPResponse
class ThirdAuthApis(viewsets.ViewSet):

    github_client_id = "6440837d0e79ec8b00fd"
    github_authorization_callback_url="http://127.0.0.1:8000/api/v1/auth/third/githubLogin"
    github_client_secret = "71dae52f731018f64df7884f395144e0e92bfe8c"
    gitee_client_id= "23dc7106d66f5a065abb2ba1ff747e69f8146d8c841c3c735e6b13f0d891026e"
    gitee_authorization_callback_url=parse.quote("http://127.0.0.1:8000/api/v1/auth/thirdgiteeLogin",safe='')
    gitee_client_secret="1707ddad487949a0b999c09a05938992f21c18db8f843d57a407a128a377930b"

    @action(methods=["GET"],detail=False,url_path="url/(?P<type>\w+)",url_name="url")  # action url_path 只允许原生正则匹配 
    def get_third_login(self,request,type):
        if type=="github":
            return HTTPResponse(
                status=status.HTTP_200_OK,
                data={"url":f"https://github.com/login/oauth/authorize?client_id={self.github_client_id}&{self.github_authorization_callback_url}"},
                app_code="oauth"
            )
        elif type=="gitee":
            return HTTPResponse(
                status=status.HTTP_200_OK,
                data={"url":f"https://gitee.com/oauth/authorize?client_id={self.gitee_client_id}&redirect_uri={self.gitee_authorization_callback_url}&response_type=code"},
                app_code="oauth"
            )
        else:
            return HTTPResponse(
                status=status.HTTP_404_NOT_FOUND,
                app_code="oauth",
                code=-1,
                message=f"暂时不支持{type}登录!"
            )

    @action(methods=["POST","GET"],detail=False,url_path="githubLogin",url_name="githubLogin") 
    def login_by_github(self,request):
        code = request.query_params.get("code",None)
        if  code:
            ...
            # https://github.com/login/oauth/authorize?client_id=6440837d0e79ec8b00fd&http://127.0.0.1:8000/v1/oauth/githubLogin
            ## 向GITHUB授权服务器申请token
            print(">>> github login",code)
            try:
                res = requests.post(
                    url="https://github.com/login/oauth/access_token",
                    params={
                        "client_id":self.github_client_id,
                        "code":code,
                        "client_secret":self.github_client_secret
                        },headers={"Accept": 'application/json'})
                    
                if res.status_code==200:
                    access_token = res.json().get("access_token",None)
                    print(res.json())
                    # if not access_token:
                    #     print(res.json())
                    #     return HttpResponseBadRequest(res.json())
                    ## get user info 
                    if access_token:
                        res = requests.get(
                            url="https://api.github.com/user",
                            headers={"Authorization": f'bearer {access_token}'}
                        )
                        print(">>> login by github -> get user info",res.json())
                        res_json = res.json()
                        oauth_id = res_json.get("id")
                        
                        record:ThirdOauthInfo = ThirdOauthInfo.objects.filter(oauth_id=oauth_id,oauth_type=4).first()
                        if not record:
                            new = ThirdOauthInfo(
                                oauth_id=oauth_id,
                                oauth_type=4,
                                oauth_count=res_json.get("login"),
                                oauth_name=res_json.get("name"),
                                oauth_avatar_url=res_json.get("avatar_url")
                                )
                            new.save()
                            return HTTPResponse(
                                code=-1,
                                message="请先绑定账号~",
                                data={"oauth_id":new.id,"is_bind":False,},
                                status=status.HTTP_404_NOT_FOUND,
                            )
                        else:
                            record.oauth_count=res_json.get("login")
                            record.oauth_name=res_json.get("name")
                            record.oauth_avatar_url=res_json.get("avatar_url")
                            if record.is_bind:
                                ## 返回账户信息
                                refresh_token = CustomTokenObtainPairSerializer.get_token(user=record.user) # 添加了自定义的token
                                user_profile = UserProfile.objects.get(user_id = record.user.id)
                                return HTTPResponse( 
                                    data= {
                                        "is_bind":True,
                                        "access_token":str(refresh_token.access_token),
                                        "refresh_token":str(refresh_token),
                                        # "permissions_dict":permissions,
                                        "profile":UserProfileSerializer(instance=user_profile).data if user_profile else None
                                    },
                                    app_code="oauth",
                                    status=status.HTTP_200_OK,
                                )
                            else:
                                return HTTPResponse(
                                    code=-1,
                                    data={
                                        "is_bind":False,
                                        "oauth_id":record.id},
                                    message="请先绑定账号~",
                                    status=status.HTTP_404_NOT_FOUND,
                                    app_code="oauth"
                                )
                    else:
                        return HTTPResponse(
                            code=-1,
                            status=status.HTTP_401_UNAUTHORIZED,
                            message=res.json().get("error_description")
                        )
            except requests.exceptions.ConnectionError as exc:
                return HTTPResponse(code=-1,message=str(exc),status=status.HTTP_408_REQUEST_TIMEOUT)

        return HTTPResponse(status=status.HTTP_200_OK,data={

        })

    @action(methods=["POST","GET"],detail=False,url_path="giteeLogin",url_name="giteeLogin") 
    def login_by_gitee(self,request):
        code = request.query_params.get("code",None)
        if  code:
            # https://gitee.com/oauth/authorize?client_id=23dc7106d66f5a065abb2ba1ff747e69f8146d8c841c3c735e6b13f0d891026e&http%3A%2F%2F127.0.0.1%3A8000%2Fv1%2Foauth%2FgiteeLogin&response_type=code
            ## 向GITEE授权服务器申请token
            try:         
                url=f"https://gitee.com/oauth/token?grant_type=authorization_code&code={code}&client_id={self.gitee_client_id}&redirect_uri={self.gitee_authorization_callback_url}&client_secret={self.gitee_client_secret}"
                res = requests.post(url)             
                if res.status_code==200:
                    access_token = res.json().get("access_token",None)
                    if not access_token:
                        return HttpResponseBadRequest(res.json())
                    else:
                        # 根据token获取用户信息
                        res = requests.get(url= "https://gitee.com/api/v5/user",params={"access_token":access_token})
                        if res.status_code==200:
                            j_res = res.json()
                            # add to user info
                            auth_info = ThirdOauthInfo.objects.filter(
                                oauth_count=j_res.get("login"),
                                oauth_type=5).first()
                            if auth_info:
                                print(">>> update third auth info")
                                auth_info.update(j_res)

                            else:
                                auth_info = ThirdOauthInfo.from_gitee(**res.json())
                                auth_info.save()

                        return Response(ResponsePayload.from_result(
                            code=status.HTTP_200_OK,
                            data=ThirdAuthInfoSerializer(auth_info).data,
                        ).to_dict(),status=status.HTTP_200_OK)
                else:
                    return HttpResponseBadRequest("get gitee authorization error!")
            except requests.exceptions.ConnectionError as exc:
                return HttpResponseForbidden(content=str(exc))

    @action(methods=("POST",),detail=False,url_name="bindAccount",url_path="bind")
    def bind_account(self,request):
        username = request.data.get("username",None)
        password = request.data.get("password",None)
        oauth_id = request.query_params.get("oauth_id",None)
        print(">>>",request.data,request.query_params)
        if not username or not password or not oauth_id:
            return  HTTPResponse(
                    code=-1,
                    status=status.HTTP_400_BAD_REQUEST,
                    message="bad request params,check username/password is not null",
                    app_code="oauth"
                )
        user = authenticate(request, username=username, password=password)
        if user:
            auth_info:ThirdOauthInfo = ThirdOauthInfo.objects.get(id=oauth_id)
            if auth_info.is_bind:
                return HTTPResponse(
                    code=-1,
                    status=status.HTTP_403_FORBIDDEN,
                    message="定了其他账号,请先进入用户中心解除绑定!",
                    app_code="oauth"
                )
            if auth_info:
                auth_info.is_bind = True
                auth_info.user = user
                auth_info.save()
                refresh_token = CustomTokenObtainPairSerializer.get_token(user=auth_info.user) # 添加了自定义的token
                user_profile = UserProfile.objects.get(user_id = auth_info.user.id)
                return HTTPResponse( 
                    data= {
                        "is_bind":True,
                        "access_token":str(refresh_token.access_token),
                        "refresh_token":str(refresh_token),
                        # "permissions_dict":permissions,
                        "profile":UserProfileSerializer(instance=user_profile).data if user_profile else None
                    },
                    app_code="oauth",
                    status=status.HTTP_200_OK,
                )
            else:
                return HTTPResponse(
                    code=-1,
                    status=status.HTTP_404_NOT_FOUND,
                    message="找不到对应的第三方用户信息,请重新授权登录!",
                    app_code="oauth"
                )
        else:
            return HTTPResponse(
                code=-1,
                status=status.HTTP_404_NOT_FOUND,
                message="账户名或密码错误!",
                app_code="oauth"
            )
        