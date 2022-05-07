from rest_framework import routers
from django.urls import path,re_path
from dataFaker.v1.views import FakerRecord,search_by_down_code

router = routers.SimpleRouter(trailing_slash=False)
# router.register("fileBroker",viewset=FileOperationViews.as_view(),basename="fileBroker")
urlpatterns = [
    path('', FakerRecord.as_view(), name='dataFaker'),  
    # path("/downCode",generate_download_code,name="downCode"),
    path("search/<str:download_code>",search_by_down_code,name="search")
]
# urlpatterns += router.urls