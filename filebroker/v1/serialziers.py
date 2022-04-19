import datetime
from hashlib import md5
from core.base import BaseSerializer
from filebroker.models import FileInfo
from rest_framework.serializers import Serializer,SerializerMethodField

class FileInfoSerializer(BaseSerializer):
    timedelta =  SerializerMethodField()
    class Meta:
        model = FileInfo
        fields = '__all__'

    
    def get_timedelta(self,obj):
        expire_time = obj.expire_time.replace(tzinfo=None).timestamp()
        now = datetime.datetime.utcnow().timestamp()
        # print(">>>>",expire_time,now)
        timedelta = int(expire_time - now)
        return timedelta


