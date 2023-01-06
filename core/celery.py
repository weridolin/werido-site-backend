
import asyncio
from celery.loaders.app import AppLoader
import os

from celery import Celery


class CeleryLoader(AppLoader):
    def on_worker_process_init(self):
        asyncio.set_event_loop(asyncio.new_event_loop())
        return super().on_worker_process_init()


# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

app = Celery('site')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')


## 配置队列
# from kombu import Queue
# app.conf.task_default_queue = 'default'  
# app.conf.task_queues = (  
#     Queue('default', routing_key='default'),
#     Queue('wechat', routing_key='wechat'),
#     Queue('weather', routing_key='weather'),

# )

# Load task modules from all registered Django apps.
app.autodiscover_tasks()


from celery_app.tasks import refresh_wechat_token, get_city_weather


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    ...
    # 刷新 wechat token
    # sender.add_periodic_task(7200-5*60, refresh_wechat_token.s(), name='refresh-wechat-token')
    # sender.add_periodic_task(10, get_city_weather.s("101010100""101010100"), name='get-weather')


app.conf.beat_schedule = {
    'scheduler1': {
        'task': 'celeryTask.wechat.get_city_weather',
        'schedule': 10.0,
        'options':{
            "queue":"get_weather"
        },
        # 'args':("101010100",)
    },
    # 'scheduler2': {
    #     'task': 'celeryTask.wechat.refresh_wechat_token',
    #     'schedule': 6,
    #     'options':{
    #         "queue":"get_wechat_token"
    #     },
    #     # 'args':("101010100",)
    # },    
}  