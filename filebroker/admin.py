from django.contrib import admin

# Register your models here.
from django.contrib import admin
from articles.models import *
from django.apps import apps
# Register your models here.
app_models=apps.get_app_config('filebroker').get_models()
for model in app_models:
    admin.site.register(model)