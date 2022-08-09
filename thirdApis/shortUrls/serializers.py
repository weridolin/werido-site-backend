from core.base import BaseSerializer
from thirdApis.models import ShortUrlRecords

class ShortUrlSerializer(BaseSerializer):
    class Meta:
        model = ShortUrlRecords
        fields = '__all__'

