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
