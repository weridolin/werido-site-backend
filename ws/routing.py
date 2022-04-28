from django.urls import path,include,re_path
from ws.data_faker_consumer import DataFakerConsumer

channel_router = [
    re_path(r'ws/dataFaker/(?P<key>\w+)$',DataFakerConsumer.as_asgi()),
    re_path(r'ws/test/dataFaker/(?P<key>\w+)$',DataFakerConsumer.as_asgi()),
]