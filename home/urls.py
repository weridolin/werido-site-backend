'''
Description: 
email: 359066432@qq.com
Author: lhj
software: vscode
Date: 2021-10-04 02:00:46
platform: windows 10
LastEditors: lhj
LastEditTime: 2021-10-05 15:26:27
'''

# from rest_framework import urlpatterns
from home.views import *
from django.urls import path,re_path
from rest_framework.routers import SimpleRouter

router = SimpleRouter(trailing_slash=False)
router.register("updatelog",UpdateLogViewSet,basename="updatelog")
router.register("comments",SiteCommentViewsSet,basename="comments")
urlpatterns=[  
    path(r"friendslinks",FriendsLinksViewsApi.as_view(),name="friendslinks"),
    path(r"backgroundImage",BackGroundMusicViews.as_view(),name="backgroundmusiclist")
    ]
urlpatterns += router.urls

# print(urlpatterns,">>>")