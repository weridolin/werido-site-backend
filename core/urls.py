'''
Description: 
email: 359066432@qq.com
Author: lhj
software: vscode
Date: 2021-04-28 15:43:58
platform: windows 10
LastEditors: lhj
LastEditTime: 2021-11-01 22:00:43
'''
"""weridoBlog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from rest_framework import routers

routers = routers.DefaultRouter()
urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/v1/",include(routers.urls)),
    path("api/v1/blogs/", include("articles.v1.urls")),
    path("api/v2/blogs/", include("articles.v2.urls")),
    path("api/v1/auth/",include("authentication.urls")),
    path("api/v1/drug/",include("drug.urls")),
    path("api/v1/home/",include("home.urls")),
    path("api/v1/fileBroker",include("filebroker.v1.urls"))
]