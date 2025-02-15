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
from django.contrib.auth import login as _login, logout as _logout, authenticate
from urllib import parse
from rest_framework_simplejwt.views import TokenBlacklistView
from rbac.permission import get_user_perms
import time
from redis.client import Redis
from django_redis import get_redis_connection
from .serializers import CustomTokenObtainPairSerializer, UserSerializer
import json
from django.apps import AppConfig
from redis import client
import requests
from rest_framework import views, viewsets, status
from rest_framework.response import Response
from django.http import HttpResponseForbidden, HttpResponseNotFound, HttpResponseBadRequest
from rest_framework import permissions
from django.contrib.auth.models import Permission, User
from authentication.models import UserProfile, ThirdOauthInfo
from authentication.v1.serializers import UserProfileSerializer, OauthInfoSerializer
from authentication.v1.singals import created_done
from rest_framework.decorators import action
from rest_framework_simplejwt.authentication import JWTAuthentication
from utils.http_ import HTTPResponse
from rest_framework.decorators import api_view, throttle_classes, permission_classes, authentication_classes
from core.base import PageNumberPaginationWrapper
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from core.base import OrderingFilterWrapper
from django_filters.rest_framework.backends import DjangoFilterBackend
import django_filters
from rbac.models import UserRoleShip


@api_view(http_method_names=["POST"])
@throttle_classes(throttle_classes=[AnonRateThrottle])
def register(request, **kwargs):
    """ 注册用户 """
    username = request.data.get("username")
    email = request.data.get("email")
    password = request.data.get("password")
    telephone = request.data.get("telephone")

    if username:
        if User.objects.filter(username=username).exists():
            return HTTPResponse(
                status=status.HTTP_400_BAD_REQUEST,
                code=-1,
                message=f"账户名 {username} 已经存在",
                app_code="auth"
            )

    if email:
        if User.objects.filter(email=email).exists():  # TODO 改成唯一
            return HTTPResponse(
                status=status.HTTP_400_BAD_REQUEST,
                code=-1,
                message=f"邮箱 {email} 已经存在",
                app_code="auth"
            )

    if telephone:
        if UserProfile.objects.filter(telephone=telephone).exists():
            return HTTPResponse(
                status=status.HTTP_400_BAD_REQUEST,
                code=-1,
                message=f"电话 {telephone} 已经存在",
                app_code="auth"
            )

    new_user = User.objects.create(username=username, email=email)
    new_user.set_password(password)  # 密码不能明文保存
    new_user.save()
    count = User.objects.count()
    created_done.send(sender=new_user.__class__, created=True,
                      instance=new_user, number=count+1, **filter_profie(request.data))
    # from core.celery import send_welcome_mail
    # send_welcome_mail.delay(receiver=email)
    return HTTPResponse(
        code=status.HTTP_200_OK, message=f"created user:{username} success!", app_code="auth"
    )


@api_view(http_method_names=["DELETE"])
@authentication_classes(authentication_classes=[JWTAuthentication])
@permission_classes(permission_classes=[permissions.IsAdminUser])
def unregister(request, **kwargs):
    """删除用户 only admin"""
    if not request.user.is_superuser:
        return HttpResponseForbidden("ONLY SUPER USER CAN OPERATE!")
    # todo admin 判断
    return Response(
        "delete",
        status=status.HTTP_200_OK
    )


class UserInfoFilter(django_filters.FilterSet):
    # title 为 request get的字段
    username = django_filters.CharFilter(
        lookup_expr="icontains", field_name="username")
    email = django_filters.CharFilter(
        lookup_expr="iexact", field_name="email")
    # tags = django_filters.CharFilter(lookup_expr="icontains", field_name = "tags__name")
    created = django_filters.DateTimeFromToRangeFilter(
        field_name="date_joined")

    class Meta:
        model = User
        fields = ["username", "email", "created"]


class UserProfileApis(viewsets.ModelViewSet):
    """"""
    # 校验登录账户
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
    pagination_class = PageNumberPaginationWrapper
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [OrderingFilterWrapper, DjangoFilterBackend]
    filterset_class = UserInfoFilter

    def destroy(self, request, *args, **kwargs):
        super().destroy(request, *args, **kwargs)
        return HTTPResponse(
            message="删除删除成功!"
        )

    def create(self, request, *args, **kwargs):
        return HTTPResponse(
            status=status.HTTP_405_METHOD_NOT_ALLOWED,
            message="no permission!"
        )

    @action(
        methods=["PUT"],
        detail=True,
        queryset=UserProfile.objects.all(),
        serializer_class=UserProfileSerializer,
        permission_classes=[permissions.IsAuthenticated]
    )
    def password(self, request, pk=None):
        """
            修改密码
        """
        if int(pk) != request.user.id and not request.user.is_staff:
            return HTTPResponse(
                status=status.HTTP_403_FORBIDDEN,
                message="当前用户没有操作权限"
            )
        try:
            new_pwd = request.data.get("new_password")
            print("modify password", pk, new_pwd)

            user = User.objects.get(id=pk)
            user.set_password(new_pwd)
            user.save()
            return HTTPResponse(
                message="重置成功"
            )
        except User.DoesNotExist:
            return HTTPResponse(
                status=status.HTTP_404_NOT_FOUND,
                message=f"未找到id为{pk}的用户"
            )

    @action(
        methods=["PUT", "GET"],
        detail=True,
        queryset=UserProfile.objects.all(),
        serializer_class=UserProfileSerializer,
        permission_classes=[permissions.IsAuthenticated]
    )
    def profile(self, request, pk=None):
        """ 修改用户信息 """
        if int(pk) != request.user.id and not request.user.is_staff:
            return HTTPResponse(
                status=status.HTTP_403_FORBIDDEN,
                message="当前用户没有操作权限"
            )
        try:
            info = UserProfile.objects.get(user_id=pk)
            if request.method == "PUT":
                # 修改用户信息
                for key, value in request.data.items():
                    if hasattr(info, key):
                        setattr(info, key, value)
                        # print(key, value)
                info.save()
                return HTTPResponse(
                    message="update success",
                    status=status.HTTP_200_OK,
                    app_code="auth")
            elif request.method == "GET":
                serializer_data = UserProfileSerializer(info)
                return HTTPResponse(
                    data=serializer_data.data,
                    app_code="auth")
        except UserProfile.DoesNotExist:
            return HTTPResponse(
                status=status.HTTP_404_NOT_FOUND,
                message=f"can not find user :{request.user.username} profile!",
                app_code="auth")

    @action(methods=["GET"], detail=False)
    def search(self, request):
        username = request.query_params.get("username", None)
        email = request.query_params.get("email", None)
        try:
            if username and username != '':
                user = User.objects.get(username=username)
            elif email and email != '':
                user = User.objects.get(email=email)
            profile_info = UserProfile.objects.get(user_id=user.id)
            serializer_data = UserProfileSerializer(profile_info)
            payload = {"data": serializer_data.data, "code": 200}
            return Response(data=payload, status=status.HTTP_200_OK)
        except (User.DoesNotExist, UserProfile.DoesNotExist):
            payload = {"data": [], "code": 404}
            return Response(data=payload, status=status.HTTP_404_NOT_FOUND)

    @action(
        methods=["POST"], 
        detail=False,
        queryset=UserProfile.objects.all(),
        serializer_class=UserProfileSerializer,
        permission_classes=[permissions.IsAuthenticated,permissions.IsAdminUser])
    def roles(self, request):
        """
            设置用户角色
        """
        user_id,role_ids = request.data.get("user_id"),request.data.get("role_id",list())
        # print(">>> set roles",user_id,role_ids)
        if not user_id:
            return HTTPResponse(
                status=status.HTTP_400_BAD_REQUEST,
                message="请先选择用户"
            )
        for role_id in role_ids:
            UserRoleShip.objects.update_or_create(role_id=role_id,user_id=user_id)
        return HTTPResponse(
            message="设置用户角色成功!"
        )



def filter_profie(info: dict):
    result = {}
    for key in UserProfile.get_db_fields():
        if key in info.keys():
            result.update({key: info.get(key)})
    return result


@api_view(http_method_names=["POST"])
def login(request, **kwargs):
    username = request.data.get("username", None)
    password = request.data.get("password", None)
    user = authenticate(request, username=username, password=password)
    if user:
        _login(request, user)
        try:
            user_profile = UserProfile.objects.get(user_id=user.id)
            roles, groups, role_perms = get_user_perms(user=user)
        except UserProfile.DoesNotExist:
            user_profile = None
        # refresh_token = RefreshToken.for_user(user) # 默认的token
        refresh_token = CustomTokenObtainPairSerializer.get_token(
            user=user)  # 添加了自定义的token
        data = {
            "access_token": str(refresh_token.access_token),
            "refresh_token": str(refresh_token),
            # "permissions_dict":permissions,
            "user_info": {
                "profile": UserProfileSerializer(instance=user_profile).data if user_profile else None,
                "permissions": role_perms,
                "roles": [role.role_name for role in roles]
            }

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


@api_view(http_method_names=['POST'])
@authentication_classes(authentication_classes=[JWTAuthentication])
def logout(request, **kwargs):
    # 此时旧的jwt-token还是有效的.清除已经注销的token?搞一个黑名单存储已经注销的token?
    # @https://github.com/jazzband/djangorestframework-simplejwt/issues/28
    # _user = request.user
    _ = _logout(request=request)  # logout之后request user会被清空
    # 清除缓存
    # conn:Redis = get_redis_connection("default") # return redis client:<redis.client.Redis>
    # conn.delete(UserBriefInfo.from_user(_user).cache_permission_key.encode())
    # jwt_token = RefreshToken.for_user(request.user)
    return HTTPResponse(
        status=status.HTTP_200_OK,
        code=0,
        app_code="auth",
        message="logout success"
    )


# 第三方登录
class ThirdAuthApis(viewsets.ViewSet):

    github_client_id = "6440837d0e79ec8b00fd"
    github_authorization_callback_url = "http://127.0.0.1:8000/api/v1/auth/third/githubLogin"
    github_client_secret = "71dae52f731018f64df7884f395144e0e92bfe8c"
    gitee_client_id = "23dc7106d66f5a065abb2ba1ff747e69f8146d8c841c3c735e6b13f0d891026e"
    gitee_authorization_callback_url = parse.quote(
        "http://127.0.0.1:8000/api/v1/auth/thirdgiteeLogin", safe='')
    gitee_client_secret = "1707ddad487949a0b999c09a05938992f21c18db8f843d57a407a128a377930b"

    # action url_path 只允许原生正则匹配
    @action(methods=["GET"], detail=False, url_path="url/(?P<type>\w+)", url_name="url")
    def get_third_login(self, request, type):
        if type == "github":
            return HTTPResponse(
                status=status.HTTP_200_OK,
                data={"url": f"https://github.com/login/oauth/authorize?client_id={self.github_client_id}&{self.github_authorization_callback_url}"},
                app_code="oauth"
            )
        elif type == "gitee":
            return HTTPResponse(
                status=status.HTTP_200_OK,
                data={"url": f"https://gitee.com/oauth/authorize?client_id={self.gitee_client_id}&redirect_uri={self.gitee_authorization_callback_url}&response_type=code"},
                app_code="oauth"
            )
        else:
            return HTTPResponse(
                status=status.HTTP_404_NOT_FOUND,
                app_code="oauth",
                code=-1,
                message=f"暂时不支持{type}登录!"
            )

    @action(methods=["POST", "GET"], detail=False, url_path="githubLogin", url_name="githubLogin")
    def login_by_github(self, request):
        code = request.query_params.get("code", None)
        if code:
            # https://github.com/login/oauth/authorize?client_id=6440837d0e79ec8b00fd&http://127.0.0.1:8000/v1/oauth/githubLogin
            # 向GITHUB授权服务器申请token
            print(">>> github login", code)
            try:
                res = requests.post(
                    url="https://github.com/login/oauth/access_token",
                    params={
                        "client_id": self.github_client_id,
                        "code": code,
                        "client_secret": self.github_client_secret
                    }, headers={"Accept": 'application/json'})

                if res.status_code == 200:
                    access_token = res.json().get("access_token", None)
                    print(res.json())
                    # if not access_token:
                    #     print(res.json())
                    #     return HttpResponseBadRequest(res.json())
                    # get user info
                    if access_token:
                        res = requests.get(
                            url="https://api.github.com/user",
                            headers={"Authorization": f'bearer {access_token}'}
                        )
                        print(">>> login by github -> get user info", res.json())
                        res_json = res.json()
                        oauth_id = res_json.get("id")
                        record: ThirdOauthInfo = ThirdOauthInfo.objects.filter(
                            oauth_id=oauth_id, oauth_type=4).first()
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
                                data={"oauth_id": new.id, "is_bind": False, },
                                status=status.HTTP_404_NOT_FOUND,
                            )
                        else:
                            record.oauth_count = res_json.get("login")
                            record.oauth_name = res_json.get("name")
                            record.oauth_avatar_url = res_json.get(
                                "avatar_url")
                            if record.is_bind:
                                # 返回账户信息
                                refresh_token = CustomTokenObtainPairSerializer.get_token(
                                    user=record.user)  # 添加了自定义的token
                                user_profile = UserProfile.objects.get(
                                    user_id=record.user.id)
                                return HTTPResponse(
                                    data={
                                        "is_bind": True,
                                        "access_token": str(refresh_token.access_token),
                                        "refresh_token": str(refresh_token),
                                        # "permissions_dict":permissions,
                                        "profile": UserProfileSerializer(instance=user_profile).data if user_profile else None
                                    },
                                    app_code="oauth",
                                    status=status.HTTP_200_OK,
                                )
                            else:
                                return HTTPResponse(
                                    code=-1,
                                    data={
                                        "is_bind": False,
                                        "oauth_id": record.id},
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
                return HTTPResponse(code=-1, message=str(exc), status=status.HTTP_408_REQUEST_TIMEOUT)

        return HTTPResponse(status=status.HTTP_200_OK, data={

        })

    @action(methods=["POST", "GET"], detail=False, url_path="giteeLogin", url_name="giteeLogin")
    def login_by_gitee(self, request):
        code = request.query_params.get("code", None)
        if code:
            # https://gitee.com/oauth/authorize?client_id=23dc7106d66f5a065abb2ba1ff747e69f8146d8c841c3c735e6b13f0d891026e&http%3A%2F%2F127.0.0.1%3A8000%2Fv1%2Foauth%2FgiteeLogin&response_type=code
            # 向GITEE授权服务器申请token
            try:
                url = f"https://gitee.com/oauth/token?grant_type=authorization_code&code={code}&client_id={self.gitee_client_id}&redirect_uri={self.gitee_authorization_callback_url}&client_secret={self.gitee_client_secret}"
                res = requests.post(url)
                if res.status_code == 200:
                    access_token = res.json().get("access_token", None)
                    if not access_token:
                        return HttpResponseBadRequest(res.json())
                    else:
                        # 根据token获取用户信息
                        res = requests.get(
                            url="https://gitee.com/api/v5/user", params={"access_token": access_token})
                        if res.status_code == 200:
                            j_res = res.json()
                            # add to user info
                            auth_info = ThirdOauthInfo.objects.filter(
                                oauth_count=j_res.get("login"),
                                oauth_type=5).first()
                            if auth_info:
                                print(">>> update third auth info")
                                auth_info.update(j_res)

                            else:
                                auth_info = ThirdOauthInfo.from_gitee(
                                    **res.json())
                                auth_info.save()

                        return Response(ResponsePayload.from_result(
                            code=status.HTTP_200_OK,
                            data=ThirdAuthInfoSerializer(auth_info).data,
                        ).to_dict(), status=status.HTTP_200_OK)
                else:
                    return HttpResponseBadRequest("get gitee authorization error!")
            except requests.exceptions.ConnectionError as exc:
                return HttpResponseForbidden(content=str(exc))

    @action(methods=("POST",), detail=False, url_name="bindAccount", url_path="bind")
    def bind_account(self, request):
        username = request.data.get("username", None)
        password = request.data.get("password", None)
        oauth_id = request.query_params.get("oauth_id", None)
        print(">>>", request.data, request.query_params)
        if not username or not password or not oauth_id:
            return HTTPResponse(
                code=-1,
                status=status.HTTP_400_BAD_REQUEST,
                message="bad request params,check username/password is not null",
                app_code="oauth"
            )
        user = authenticate(request, username=username, password=password)
        if user:
            auth_info: ThirdOauthInfo = ThirdOauthInfo.objects.get(id=oauth_id)
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
                refresh_token = CustomTokenObtainPairSerializer.get_token(
                    user=auth_info.user)  # 添加了自定义的token
                user_profile = UserProfile.objects.get(
                    user_id=auth_info.user.id)
                return HTTPResponse(
                    data={
                        "is_bind": True,
                        "access_token": str(refresh_token.access_token),
                        "refresh_token": str(refresh_token),
                        # "permissions_dict":permissions,
                        "profile": UserProfileSerializer(instance=user_profile).data if user_profile else None
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
