from rest_framework import routers
from django.urls import path,re_path
from wechat.v1.apis import PublicCountMessageApis

router = routers.SimpleRouter(trailing_slash=True)
router.register("public/message",viewset=PublicCountMessageApis,basename="wechat-public-count-message")
# router.register("perms",viewset=PermissionApis,basename="rbac-perms")
urlpatterns = [
    # path("menus",MenuApis.as_view(),name="rbac-menu")
]
urlpatterns += router.urls

print("wechat apis --->  ",urlpatterns)