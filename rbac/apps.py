from asyncio.log import logger
from django.apps import AppConfig,apps

class RbacConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'rbac'

    def ready(self) -> None:
        from rbac.models import Role
        from rbac.models import ModelOperation,UserRoleShip,Permissions,RolePermissionShip
        from rbac.apis import add_permission
        from django.contrib.auth.models import User

        ## 为各个model添加增删改查的权限
        # for app_label in apps.all_models.keys():
        #     if app_label in ['authentication', 'thirdApis', 'rbac', 'articles', 'drug', 'home', 'filebroker', 'celery_app', 'dataFaker']:
        #     # if app_label in ['dataFaker']:
        #         print(f"初始化app({app_label})中所有model的操作权限...")
        #         for name,instance in apps.all_models[app_label].items():
        #             add_permission(orm=ModelOperation,app_label=app_label,op_name=f"view",op_model_name=name,description=f"对表:{name}查询的权限")
        #             add_permission(orm=ModelOperation,app_label=app_label,op_name=f"delete",op_model_name=name,description=f"对表:{name}删除的权限")
        #             add_permission(orm=ModelOperation,app_label=app_label,op_name=f"post",op_model_name=name,description=f"对表:{name}增加的权限")
        #             add_permission(orm=ModelOperation,app_label=app_label,op_name=f"update",op_model_name=name,description=f"对表:{name}修改的权限")                    


        # ## 初始化角色
        # print("初始化角色信息...")
        # super_role,_ = Role.objects.update_or_create(role_name="超级管理员")
        # guest_role,_ = Role.objects.update_or_create(role_name="游客")
        
        # # 为超级管理员添加权限 
        # print("为超级管理员添加所有的权限")
        # all_permissions =  Permissions.objects.all()
        # for permission in all_permissions:
        #     RolePermissionShip.objects.update_or_create(role_id=super_role.id,permission_id=permission.id)
        #     RolePermissionShip.objects.update_or_create(role_id=guest_role.id,permission_id=permission.id)

        # # 为所有超级用户添加超级管理员角色·
        # print("为超级用户添加超级用户角色")
        # all_super_user = User.objects.filter(is_superuser=True).all()
        # for super_user in all_super_user:
        #     UserRoleShip.objects.update_or_create(
        #         user_id = super_user.id,
        #         role_id = super_role.id
        #     )

        return super().ready()