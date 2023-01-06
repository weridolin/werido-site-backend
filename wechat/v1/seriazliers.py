from core.base import BaseSerializer
from wechat.models import WechatMessage

class WechatMessageSerializer(BaseSerializer):

    class Meta:
        model = WechatMessage
        fields = '__all__'
        depth = 1
        # extra_kwargs = {
        #     "menu_name": {
        #         "error_messages": {
        #             "required": _("菜单名字不能为空!")
        #         }
        #     },
        #     "menu_url": {
        #         "error_messages": {
        #             "required": _("菜单url不能为空!"),
        #             # "unique": _("菜单url已经存在") todo
                    
        #         }
        #     },
        #     "menu_type": {
        #         "error_messages": {
        #             "required": _("菜单类型不能为空!")
        #         }
        #     }
        # }