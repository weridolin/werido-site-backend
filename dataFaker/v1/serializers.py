import datetime

from core.base import BaseSerializer
from dataFaker.models import DataFakerRecordInfo
from rest_framework.serializers import Serializer,SerializerMethodField

class DataFakerRecordInfoSerializer(BaseSerializer):
    timedelta =  SerializerMethodField()
    class Meta:
        model = DataFakerRecordInfo
        fields = '__all__'

    
    def get_timedelta(self,obj):
        expire_time = obj.expire_time.replace(tzinfo=None).timestamp()
        now = datetime.datetime.utcnow().timestamp()
        # print(">>>>",expire_time,now)
        timedelta = int(expire_time - now)
        return timedelta


