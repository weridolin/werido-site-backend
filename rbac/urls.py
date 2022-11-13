from rest_framework import routers
from django.urls import path,re_path
from rbac.apis import MenuApis

router = routers.SimpleRouter(trailing_slash=False)
# router.register("menus/",viewset=MenuApis.as_view(),basename="rbac-menu")

urlpatterns = [
    path("menus/",MenuApis.as_view(),name="rbac-menu")
]
urlpatterns += router.urls