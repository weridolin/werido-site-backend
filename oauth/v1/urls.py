from django.db import router
from django.urls import path,re_path
from oauth.v1.apis import (
    ApplicationRegisterViews,
    ApplicationResourceViews,
    AuthorizationView,
    TokenAccessViews,
    RevokeTokenViews,
    UserInfoByOauthViews
)


urlpatterns = [
    path(r"/applications/register", ApplicationRegisterViews.as_view(), name="register"),
    re_path(r"^/authorize/$",AuthorizationView.as_view(),name="authorize"),
    re_path(r"^/token/$", TokenAccessViews.as_view(), name="token"),
    re_path(r"^/revoke_token/$", RevokeTokenViews.as_view(), name="revoke-token"),
    re_path(r"^/userInfo/$", UserInfoByOauthViews.as_view(), name="user-info"),    
]

from rest_framework.routers import DefaultRouter,SimpleRouter
router = DefaultRouter()
router.register(r"/application/resource",ApplicationResourceViews,basename="app_resource")
urlpatterns+=router.urls