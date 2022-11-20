from rest_framework import routers
from django.urls import path,re_path
from rbac.apis import MenuApis


# trailing_slash=True 会在生成的url后面自动加上斜杠
router = routers.SimpleRouter(trailing_slash=True)
router.register("menus",viewset=MenuApis,basename="rbac-menu")

urlpatterns = [
    # path("menus",MenuApis.as_view(),name="rbac-menu")
]
urlpatterns += router.urls