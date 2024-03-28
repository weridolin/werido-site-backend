from django.urls import path,re_path
from rest_framework import routers
from thirdApis.gpt.apis import GptConversationViewsSet,GptMessageViewSet

from core.routers import SupportDeletedAllRouter
from rest_framework.routers import DefaultRouter

router = SupportDeletedAllRouter(trailing_slash=False)
router.register("conversation",viewset=GptConversationViewsSet,basename="gpt-conversation")
router.register("message",viewset=GptMessageViewSet,basename="gpt-message")


gpt_urls = [
]
gpt_urls+=router.urls

urlpatterns = gpt_urls
# print(urlpatterns)