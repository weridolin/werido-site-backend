from rest_framework import routers
from django.urls import path,re_path
from filebroker.v1.views import FileOperationViews,generate_download_code,search_by_down_code

urlpatterns = [
    path('', FileOperationViews.as_view(), name='fileBroker'),  
    path("/downCode",generate_download_code,name="downCode"),
    path("/search/<str:download_code>",search_by_down_code,name="search")
]
