
from datetime import datetime
from core.base import BaseSerializer
from thirdApis.models import ShortUrlRecords
from rest_framework import serializers
class ShortUrlSerializer(BaseSerializer):
    expire_time = serializers.SerializerMethodField(method_name="get_expire_time")
    class Meta:
        model = ShortUrlRecords
        fields = '__all__'

    def get_expire_time(self,obj):
        return datetime.strftime(obj.expire_time,"%Y-%m-%d %H:%M:%S")
