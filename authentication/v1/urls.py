'''
Description: 
email: 359066432@qq.com
Author: lhj
software: vscode
Date: 2021-09-11 14:47:01
platform: windows 10
LastEditors: lhj
LastEditTime: 2021-09-19 14:50:58
'''
from rest_framework import routers
from django.urls import path,re_path
from .api import UserProfileApis,ThirdAuthApis,register,unregister,login,logout
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView
from authentication.v1.serializers import CustomTokenObtainPairSerializer,CustomTokenObtainPairView
from rest_framework_simplejwt.views import TokenBlacklistView

router = routers.SimpleRouter(trailing_slash=False)
router.register("user",viewset=UserProfileApis,basename="user")
# router.register("",viewset=AuthApis,basename="auth")
router.register("third",viewset=ThirdAuthApis,basename="thirdAuth")

urlpatterns = [
    path('login/',login,name="login"),
    path('logout/',logout,name="logout"),    
    path('register/',register,name="register-new-user"),
    path('unregister/',unregister,name="delete_user"),
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/blacklist/', TokenBlacklistView.as_view(), name='token_blacklist'), # 让refresh token失效
]
urlpatterns += router.urls
