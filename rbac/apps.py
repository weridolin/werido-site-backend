from asyncio.log import logger
from django.apps import AppConfig, apps


class RbacConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'rbac'

    def ready(self) -> None:
        from rbac.models import Role
        from rbac.models import ModelOperation, UserRoleShip, Permissions, RolePermissionShip, Menu
        from rbac.apis import add_model_op_permission
        from django.contrib.auth.models import User

        # # 为各个model添加增删改查的权限
        # for app_label in apps.all_models.keys():
        #     if app_label in ['authentication', 'thirdApis', 'rbac', 'articles', 'drug', 'home', 'filebroker', 'celery_app', 'dataFaker']:
        #         print(f"初始化app({app_label})中所有model的操作权限...")
        #         for name,instance in apps.all_models[app_label].items():
        #             add_model_op_permission(app_label=app_label,op_name=f"view",op_model_name=name,description=f"对表:{name}查询的权限")
        #             add_model_op_permission(app_label=app_label,op_name=f"delete",op_model_name=name,description=f"对表:{name}删除的权限")
        #             add_model_op_permission(app_label=app_label,op_name=f"post",op_model_name=name,description=f"对表:{name}增加的权限")
        #             add_model_op_permission(app_label=app_label,op_name=f"update",op_model_name=name,description=f"对表:{name}修改的权限")

        # # 添加 菜单
        print("添加默认菜单......")
        self.add_default_menu()

        # ## 初始化角色
        print("初始化角色信息...")
        super_role,_ = Role.objects.update_or_create(role_name="超级管理员")
        guest_role,_ = Role.objects.update_or_create(role_name="游客")
        guest_role,_ = Role.objects.update_or_create(role_name="普通用户") 

        ## 为普通用户添加菜单权限

        
        # # 为超级管理员添加权限
        # print("为超级管理员添加所有的权限")
        # all_permissions =  Permissions.objects.all()
        # for permission in all_permissions:
        #     print("add permission",permission)
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

    def add_default_menu(self):
        default_menu_info = [
            {
                "menu_name": "权限管理",
                "menu_url": "/admin/permissions",
                "menu_route_name": "adminPermissions",
                "menu_icon": "Lock",
                "menu_type": 0,
                "menu_view_path": "PermissionManager.vue",
                "children": [
                    {
                        "menu_name": "菜单管理",
                        "menu_url": "/admin/permissions/menus",
                        "menu_route_name": "adminPermissionsMenus",
                        "menu_icon": "Menu",
                        "menu_type": 0,
                        "menu_view_path": "MenuManager.vue",
                        "children": []
                    },
                    {
                        "menu_name": "数据库管理",
                        "menu_url": "/admin/permissions/models",
                        "menu_route_name": "adminPermissionsModelsOp",
                        "menu_icon": "List",
                        "menu_type": 0,
                        "menu_view_path": "ModelOpManager.vue",
                        "children": []
                    },
                    {
                        "menu_name": "角色管理",
                        "menu_url": "/admin/permissions/roles",
                        "menu_route_name": "adminPermissionsRoles",
                        "menu_icon": "UserFilled",
                        "menu_type": 0,
                        "menu_view_path": "RoleManager.vue",
                        "children": []
                    },
                ]
            },
            {
                "menu_name": "用户管理",
                "menu_url": "/admin/users",
                "menu_route_name": "adminUserManager",
                "menu_icon": "User",
                "menu_type": 0,
                "menu_view_path": "UserManager.vue",
                "children": []
            },
            {
                "menu_name": "个人档案",
                "menu_url": "/admin/profile",
                "menu_route_name": "UserProfile",
                "menu_icon": "User",
                "menu_type": 0,
                "menu_view_path": "UserProfile.vue",
                "children": []
            }
                    
        ]

        def _add_menu(menu_info, p_id=None):
            from rbac.apis import add_menu
            menu = add_menu(
                menu_icon=menu_info["menu_icon"],
                menu_type=menu_info["menu_type"],
                menu_url=menu_info["menu_url"],
                menu_view_path=menu_info["menu_view_path"],
                menu_name=menu_info["menu_name"],
                menu_route_name=menu_info["menu_route_name"],
                p_id=p_id)
            for child_menu_info in menu_info["children"]:
                _add_menu(child_menu_info, p_id=menu)

        for menu_info in default_menu_info:
            _add_menu(menu_info)
