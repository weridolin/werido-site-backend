from django.db import router
from django.urls import path,re_path
from oauth.v1.apis import ApplicationRegisterViews,ApplicationResourceViews

urlpatterns = [
    path(r"/applications/register", ApplicationRegisterViews.as_view(), name="register"),
]

from rest_framework.routers import DefaultRouter,SimpleRouter
router = DefaultRouter()
router.register(r"/application/resource",ApplicationResourceViews,basename="app_resource")
urlpatterns+=router.urls