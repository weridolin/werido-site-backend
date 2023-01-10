from django.apps import AppConfig
from utils.redis_keys import WECHAT
import requests

class WechatConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'wechat'


    def ready(self) -> None:
        # 生成菜单
        from redis.client import Redis
        from django_redis import get_redis_connection
        from core import settings
        conn:Redis = get_redis_connection()
        access_token = conn.get(WECHAT.access_token_key())
        if access_token:
            print(access_token)
        return super().ready()