from core.base import BaseSerializer
from rbac.models import Menu

class MenuSerializer(BaseSerializer):

    class Meta:
        model = Menu
        fields = '__all__'
