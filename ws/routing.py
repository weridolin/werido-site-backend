from django.urls import path,include,re_path
from ws.data_faker_consumer import DataFakerConsumer
from ws.chatGPT_comsumer import ChatGPTMessageConsumer

channel_router = [
    re_path(r'ws/dataFaker/(?P<key>\w+)$',DataFakerConsumer.as_asgi()),
    re_path(r'ws/test/dataFaker/(?P<key>\w+)$',DataFakerConsumer.as_asgi()),
    re_path(r'ws/thirdApi/chatGPT/(?P<user_id>\w+)$',ChatGPTMessageConsumer.as_asgi())

]