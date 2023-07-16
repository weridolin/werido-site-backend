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
from asyncio import tasks
from django.contrib import admin
from django.urls import path,include,re_path
from rest_framework import routers
from ws.data_faker_consumer import DataFakerConsumer
# from oauth2_provider.urls
import time
from rest_framework.decorators import api_view
from rest_framework.response  import Response
from django_celery_beat.models import PeriodicTask, IntervalSchedule
import json

@api_view(["GET"])
def celery_test(request):
    # from core.celery import test
    # res = test.delay(2222)
    # print(res.get())
    # return Response("test")
    ...
    # schedule, created = IntervalSchedule.objects.get_or_create(every=1,period=IntervalSchedule.SECONDS)
    # tasks, created = PeriodicTask.objects.get_or_create(
    #     interval=schedule,                  # we created this above.
    #     name='TestTask1-2',          # simply describes this periodic task.
    #     task='core.celery.test_task',  # name of task.
    #     args=json.dumps([8]),
    # )
    # tasks.enabled=False
    # tasks.save()
    for i in range(10):
        time.sleep(1)
        print(">>>>>",i)
    return Response("Ssss")

def test_task(count):
    for i in count:
        print(i,">>>>>>>>>>>>>>>")



routers = routers.DefaultRouter()
urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/v1/",include(routers.urls)),
    path("blogs/api/v1/", include("articles.v1.urls")),
    path("blogs/api/v2/", include("articles.v2.urls")),
    # path("api/v1/auth/",include("authentication.v1.urls")),
    path("drug/api/v1/",include("drug.urls")),
    path("home/api/v1/",include("home.urls")),
    path("fileBroker/api/v1/",include("filebroker.v1.urls")),
    path("dataFaker/api/v1/",include("dataFaker.v1.urls")),
    # path("api/v1/oauth", include('oauth.v1.urls')),
    # path("third/api/v1",include('thirdApis.urls')),
    # path("api/oauth/test/",include('oauth2_provider.urls')),
    # path("api/celeryTest",celery_test),
    # path("api/v1/rbac/",include('rbac.urls')),
    path("covid19/api/v1/",include('covid19.v1.urls')),
    path("wechat/api/v1/",include('wechat.v1.urls')),
    path("shortUrl/api/v1/",include('thirdApis.shortUrls.urls')),
    path("apiCollector/api/v1/",include('thirdApis.apiCollector.urls')),
    path("chatGPT/api/v1/",include('thirdApis.chatGPT.urls'))


]



