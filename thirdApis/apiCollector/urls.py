from django.urls import path,re_path
from thirdApis.apiCollector.apis import TaskOperationView


api_collector_urls = [
    path(r"/apiCollector/task", TaskOperationView.as_view(), name="api-collector-task"),
]
