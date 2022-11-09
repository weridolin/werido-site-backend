
from datetime import datetime
from core.base import BaseSerializer
from thirdApis.models import ApiCollectorSpiderRunRecord, ApiCollector, ApiCollectorSpiderResourceModel
from rest_framework import serializers


class ApiCollectorSpiderRunRecordSerializer(BaseSerializer):
    finish_time = serializers.SerializerMethodField(
        method_name="get_finish_time")

    class Meta:
        model = ApiCollectorSpiderRunRecord
        fields = '__all__'

    def get_finish_time(self, obj):
        return datetime.strftime(obj.finish_time, "%Y-%m-%d %H:%M:%S")


class ApiInfoSerializer(BaseSerializer):
    expire_time = serializers.SerializerMethodField(
        method_name="get_expire_time")

    class Meta:
        model = ApiCollector
        fields = '__all__'

    def __init__(self, instance=None, data=..., **kwargs):
        self.types = list()
        super().__init__(instance, data, **kwargs)

    def get_expire_time(self, obj):
        return int(obj.expire_time.timestamp())


class ApiCollectorSpiderResourceSerializer(BaseSerializer):
    last_run_time = serializers.SerializerMethodField(
        method_name="get_last_run_time")
    is_running = serializers.SerializerMethodField(
        method_name="get_is_running")

    class Meta:
        model = ApiCollectorSpiderResourceModel
        fields = '__all__'

    def __init__(self, running_records=None, instance=None, data=..., **kwargs):
        if running_records:
            self.running_spider_names = [
                record.name for record in running_records]
        else:
            self.running_spider_names=[]
        super().__init__(instance, data, **kwargs)

    def get_last_run_time(self, obj):
        if obj.last_run_time:
            return datetime.strftime(obj.last_run_time, "%Y-%m-%d %H:%M:%S")
        else:
            return "未运行过"

    def get_is_running(self, obj):
        if obj.name in self.running_spider_names:
            return True
        return False
