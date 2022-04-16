from hashlib import md5
from core.base import BaseSerializer
from filebroker.models import FileInfo
from rest_framework.serializers import Serializer

class FileInfoSerializer(BaseSerializer):
        class Meta:
            model = FileInfo
            fields = '__all__'



