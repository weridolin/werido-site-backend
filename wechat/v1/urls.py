from rest_framework import routers
from django.urls import path,re_path
from wechat.v1.apis import PublicCountMessageApis



class WeChatApisRouter(routers.SimpleRouter):
    ## 自定义下路由，把 delete 单个object改成 删除多个
    routes = [
        # List route.
        routers.Route(
            url=r'^{prefix}{trailing_slash}$',
            mapping={
                'get': 'retrieve',
                # 'get': 'list',
                'post': 'create',
                'delete': 'destroy'
            },
            name='{basename}-list',
            detail=False,
            initkwargs={'suffix': 'List'}
        ),
        # Dynamically generated list routes. Generated using
        # @action(detail=False) decorator on methods of the viewset.
        routers.DynamicRoute(
            url=r'^{prefix}/{url_path}{trailing_slash}$',
            name='{basename}-{url_name}',
            detail=False,
            initkwargs={}
        ),
        # Detail route.
        routers.Route(
            url=r'^{prefix}/{lookup}{trailing_slash}$',
            mapping={
                # 'get': 'retrieve',
                'put': 'update',
                'patch': 'partial_update',
                # 'delete': 'destroy'
            },
            name='{basename}-detail',
            detail=True,
            initkwargs={'suffix': 'Instance'}
        ),
        # Dynamically generated detail routes. Generated using
        # @action(detail=True) decorator on methods of the viewset.
        routers.DynamicRoute(
            url=r'^{prefix}/{lookup}/{url_path}{trailing_slash}$',
            name='{basename}-{url_name}',
            detail=True,
            initkwargs={}
        ),
    ]  

router = WeChatApisRouter(trailing_slash=True)
router.register("public/message",viewset=PublicCountMessageApis,basename="wechat-public-count-message")
# router.register("perms",viewset=PermissionApis,basename="rbac-perms")
urlpatterns = [
    # path("menus",MenuApis.as_view(),name="rbac-menu")
]
urlpatterns += router.urls

print("wechat apis --->  ",urlpatterns)