'''
Description: 
email: 359066432@qq.com
Author: lhj
software: vscode
Date: 2021-04-28 15:43:58
platform: windows 10
LastEditors: lhj
LastEditTime: 2021-09-04 12:21:31
'''
"""
ASGI config for weridoBlog project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/asgi/
"""


import os
from django.core.asgi import get_asgi_application
from django.urls import re_path
from ws.routing import channel_router
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

# Initialize Django ASGI application early to ensure the AppRegistry
# is populated before importing code that may import ORM models.
django_asgi_app = get_asgi_application()


from channels.routing import ProtocolTypeRouter,URLRouter

application = ProtocolTypeRouter({
  "http": django_asgi_app,
  "websocket": URLRouter(channel_router),
})

# ## learn asgi
# from channels.generic.http import AsyncHttpConsumer

# class MyAsyncHttpConsumer(AsyncHttpConsumer):
#   ...
#   async def handle(self, body):
#     print(">>> 处理body",body)
#     await self.send_response(200, b"this is response", 
#       headers=[
#         (b"Content-Type", b"text/plain"),
#     ])
  


# async def async_app(scope,receive,send):
#     print("get scope >>>",scope)
#     event = await receive()
#     print("get event >>>",event)
#     # await asyncio.sleep(10)
#     await send({
#             'type': 'http.response.start',   # 响应头的信息通过这个事件返回，必须发生在body发送之前
#             'status': 200,
#             'headers': [
#                 [b'content-type', b'application/json'],
#         ]   # 发送响应体内容事件
#     })
#     await send({
#         'type': 'http.response.body',   # 发送响应体内容事件
#         'body': "response part1".encode("utf-8"),
#         'more_body': True  # 代表后面还有消息要返回
#     })
#     # await asyncio.sleep(3) # 不能使用time.sleep, 会阻塞整个线程
#     await send({
#         'type': 'http.response.body',
#         'body': "response part2".encode("utf-8"),
#         'more_body': False # 已经没有内容了，请求可以结束了
#     })
#     # event = await receive()
#     print("get event >>>",event)

# application = ProtocolTypeRouter({
#   # "http": URLRouter([
#   #     re_path(r'test',MyAsyncHttpConsumer.as_asgi())]),
#     "http": URLRouter([
#       re_path(r'test',async_app)]),
#   "websocket": URLRouter(channel_router),
# })