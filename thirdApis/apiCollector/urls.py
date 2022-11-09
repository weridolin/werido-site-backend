from django.urls import path,re_path
from rest_framework import routers
from thirdApis.apiCollector.apis import TaskOperationView,ApiInfoViews,ApisSpiderResourceViews

router = routers.SimpleRouter(trailing_slash=False)
router.register("/apiCollector/apiInfo",viewset=ApiInfoViews,basename="api-info")
# router.register("/apiCollector/apiResource",viewset=ApisSpiderResourceViews.as_view(),basename="api-resource")

api_collector_urls = [
    path(r"/apiCollector/task", TaskOperationView.as_view(), name="api-collector-task"),
    path(r"/apiCollector/apiResource",ApisSpiderResourceViews.as_view(),name="api-resource")
]


api_collector_urls += router.urls

