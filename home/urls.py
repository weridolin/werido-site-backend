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
from home.views import UpdateLogViewSet,FriendsLinksViewsApi,BackGroundMusicViews,BackImagesViews,SiteCommentViewsSet
from django.urls import path,re_path
from rest_framework.routers import SimpleRouter

router = SimpleRouter(trailing_slash=False)
router.register("updatelog",UpdateLogViewSet,basename="updatelog")
router.register("comments",SiteCommentViewsSet,basename="comments")
router.register("backGroundImages",BackImagesViews,basename="backGroundImages")
urlpatterns=[  
    path(r"friendslinks",FriendsLinksViewsApi.as_view(),name="friendslinks"),
    path(r"backGroundMusic",BackGroundMusicViews.as_view(),name="backGroundMusic"),
    # path(r"backGroundImages",BackImagesViews.as_view(),name="backGroundImages")

    # path(r"image/<str:filename>",BackImagesViews.as_view(),name="backGroundImages)
    ]
urlpatterns += router.urls

# print(urlpatterns,">>>")