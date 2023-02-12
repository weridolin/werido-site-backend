from django.urls import path,re_path
from rest_framework import routers
from thirdApis.chatGPT.apis import ChatGPTConversationViewsSet,ChatGPTMessageViewSet


router = routers.SimpleRouter(trailing_slash=False)
router.register("/chatGPT/conversation",viewset=ChatGPTConversationViewsSet,basename="chatGPT-conversation")
router.register("/chatGPT/message",viewset=ChatGPTMessageViewSet,basename="chatGPT-message")


chatGPT_urls = []
chatGPT_urls+=router.urls