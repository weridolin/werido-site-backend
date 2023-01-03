from core.base import BaseSerializer
from rbac.models import Menu,Role,ModelOperation,Permissions
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

class MenuSerializer(BaseSerializer):

    # menu_name = models.CharField(max_length=128,null=False,help_text="菜单名称",verbose_name="菜单名称")
    # menu_url = models.CharField(max_length=128,null=False,help_text="菜单url",verbose_name="菜单url",unique=True)
    # menu_icon = models.CharField(max_length=128,null=True,help_text="菜单对应的vue-icon",verbose_name="菜单对应的Vue-icon")
    # menu_type = models.SmallIntegerField(null=False,default=0,help_text="菜单类型:0菜单 1按钮",verbose_name="菜单类型:0菜单 1按钮")
    # menu_view_path = models.CharField(max_length=128,null=True,help_text="菜单对应的page路径",verbose_name="菜单对应的page路径")
    # menu_route_name = models.CharField(max_length=128,null=True,help_text="路由名称",verbose_name="路由名称")
    # p_id = models.ForeignKey("Menu",null=True,help_text="父级菜单",verbose_name="父级菜单",on_delete=models.CASCADE)

    # menu_name = serializers.CharField(required=True, error_messages={'required': u'菜单名字不能为空!'})
    # menu_url = serializers.CharField(error_messages={'unique': u'该菜单url已经存在!'},required=True)
    # menu_icon = serializers.CharField()
    # menu_type = serializers.IntegerField(required=True)
    # menu_view_path= serializers.CharField(required=True)
    # menu_route_name= serializers.CharField(required=True)
    # p_id=serializers.CharField(required=True)

    class Meta:
        model = Menu
        fields = '__all__'
        depth = 1
        extra_kwargs = {
            "menu_name": {
                "error_messages": {
                    "required": _("菜单名字不能为空!")
                }
            },
            "menu_url": {
                "error_messages": {
                    "required": _("菜单url不能为空!"),
                    # "unique": _("菜单url已经存在") todo
                    
                }
            },
            "menu_type": {
                "error_messages": {
                    "required": _("菜单类型不能为空!")
                }
            }
        }

        # validators = [
        #     serializers.UniqueTogetherValidator(
        #         queryset=Menu.objects.all(),
        #         fields=('menu_url'),
        #         message="菜单url已经存在"
        #     )
        # ]


    # def validate(self, attrs):
    #     print(attrs)
    #     return super().validate(attrs)

    # def validate_menu_url(self, obj): 
    #     # modelSerializer会定义好了 validate 方法
    #     print(">>> validate menu url")
    #     # today = date.today()
    #     # age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
    #     # if (not(20 < age < 30)):
    #     #     raise serializers.ValidationError("You are no eligible for the job")
    #     return obj

    def create(self, validated_data):
        # print("create menu", validated_data)
        instance =  super().create(validated_data)
        # 插入到对用permission表中
        Permissions.objects.update_or_create(
            permission_id = instance.id,
            permission_type="menu"
        )
        return instance

    def update(self, instance, validated_data):
        # print("update men)
        return super().update(instance, validated_data)
        # print(instance.id,"create menu success")
        # return instance




class RoleSerializer(BaseSerializer):
    class Meta:
        model = Role
        fields = '__all__'
        depth = 1
        extra_kwargs = {
            "role_name": {
                "error_messages": {
                    "required": _("角色名称不能为空!"),
                    # "unique": _("菜单url已经存在") todo
                }
            }
        }


class PermissionSerializer(BaseSerializer):
    ...


class ModelAccessSerializer(BaseSerializer):

    class Meta:
        model = ModelOperation
        fields = '__all__'
        depth = 1
        extra_kwargs = {
            "app_label": {
                "error_messages": {
                    "required": _("所属模块不能为空!"),
                    # "unique": _("菜单url已经存在") todo
                }
            },
            "op_name": {
                "error_messages": {
                    "required": _("操作名称不能为空!"),
                    # "unique": _("菜单url已经存在") todo
                }
            },
            "op_model_name": {
                "error_messages": {
                    "required": _("操作的表不能为空!"),
                    # "unique": _("菜单url已经存在") todo
                }
            }
        }