
from datetime import datetime
from core.base import BaseSerializer
from thirdApis.models import ApiCollectorSpiderRunRecord,ApiCollector
from rest_framework import serializers


class ApiCollectorSpiderRunRecordSerializer(BaseSerializer):
    finish_time = serializers.SerializerMethodField(method_name="get_finish_time")
    class Meta:
        model = ApiCollectorSpiderRunRecord
        fields = '__all__'

    def get_finish_time(self,obj):
        return datetime.strftime(obj.finish_time,"%Y-%m-%d %H:%M:%S")
