from django.urls import path,include,re_path
from ws.data_faker_consumer import DataFakerConsumer
from ws.chatGPT_comsumer import ChatGPTMessageConsumer

channel_router = [
    re_path(r'dataFaker/ws/(?P<key>\w+)$',DataFakerConsumer.as_asgi()),
    re_path(r'ws/test/dataFaker/(?P<key>\w+)$',DataFakerConsumer.as_asgi()),
    re_path(r'chatGPT/ws/(?P<user_id>\w+)$',ChatGPTMessageConsumer.as_asgi())

]