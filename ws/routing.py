from django.urls import path,include,re_path
from ws.data_faker_consumer import DataFakerConsumer
from ws.gpt_consumer import GptMessageConsumer

channel_router = [
    re_path(r'dataFaker/ws/(?P<key>\w+)$',DataFakerConsumer.as_asgi()),
    re_path(r'ws/test/dataFaker/(?P<key>\w+)$',DataFakerConsumer.as_asgi()),
    re_path(r'Gpt/ws/(?P<user_id>\w+)$',GptMessageConsumer.as_asgi())

]