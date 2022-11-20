from email.policy import default
from tokenize import group
from django.db import models
from core.base import BaseModel
from django.contrib.auth.models import User
# Create your models here.

# @https://zhuanlan.zhihu.com/p/63769951

class Group(BaseModel):
    
    class Meta:
        db_table = "rbac_group"
        verbose_name = "rbac_用户组"
        verbose_name_plural = "rbac_用户组"

    group_name = models.CharField(max_length=128,null=False,help_text="用户组名称",verbose_name="用户组名称")
    p_id = models.IntegerField(null=False,default=-1,help_text="父用户组名称",verbose_name="父用户组名称")


class UserGroupShip(BaseModel):
    class Meta:
        db_table = "rbac_group_user"
        verbose_name = "rbac_组与用户关联表"
        verbose_name_plural = "rbac_组与用户关联表"   
        unique_together = ('group_id', 'user_id') 

    group_id = models.IntegerField(null=False,help_text="用户组id",verbose_name="用户组id",db_index=True)
    user_id = models.IntegerField(null=False,help_text="用户id",verbose_name="用户id",db_index=True)


class Role(BaseModel):
    class Meta:
        db_table = "rbac_role"
        verbose_name = "rbac_用户角色"
        verbose_name_plural = "rbac_用户角色"

    role_name = models.CharField(max_length=128,null=False,help_text="用户角色",verbose_name="用户角色",unique=True)
    # p_id = models.IntegerField(null=False,default=-1,help_text="父用户组名称",verbose_name="父用户组名称")   # 考虑角色继承？ RBAC1引入了角色继承

    # RBAC1，基于RBAC0模型，引入角色间的继承关系，即角色上有了上下级的区别，角色间的继承关系可分为一般继承关系和受限继承关系。
    # 一般继承关系仅要求角色继承关系是一个绝对偏序关系，允许角色间的多继承。而受限继承关系则进一步要求角色继承关系是一个树结构，实现角色间的单继承。


class UserPermissionShip(BaseModel):
    class Meta:
        db_table = "rbac_user_permission"
        verbose_name = "rbac_用户与权限关联表"
        verbose_name_plural = "rbac_用户与权限关联表"   
        unique_together = ('permission_id', 'user_id') 

    
    permission_id = models.IntegerField(null=False,help_text="对应权限内容表的id",verbose_name="对应权限内容表的id",db_index=True)
    user_id = models.IntegerField(null=False,help_text="用户id",verbose_name="用户id",db_index=True)    

class GroupRoleShip(BaseModel):
    class Meta:
        db_table = "rbac_group_role"
        verbose_name = "rbac_组与角色关联表"
        verbose_name_plural = "rbac_组与角色关联表" 
        unique_together = ('role_id', 'group_id') 

    
    group_id = models.IntegerField(null=False,help_text="用户组id",verbose_name="用户组id",db_index=True)
    role_id = models.IntegerField(null=False,help_text="角色id",verbose_name="角色id",db_index=True)


class UserRoleShip(BaseModel):
    class Meta:
        db_table = "rbac_user_role"
        verbose_name = "rbac_用户与角色关联表"
        verbose_name_plural = "rbac_用户与角色关联表"  
        unique_together = ('role_id', 'user_id') 
    
    user_id = models.IntegerField(null=False,help_text="用户id",verbose_name="用户id",db_index=True)
    role_id = models.IntegerField(null=False,help_text="角色id",verbose_name="角色id",db_index=True)



class Permissions(BaseModel):
    class Meta:
        db_table = "rbac_permission"
        verbose_name = "rbac_权限表"
        verbose_name_plural = "rbac_权限表" 
        unique_together = ('permission_id', 'permission_type') 
    
    permission_id = models.IntegerField(null=False,help_text="对应权限种类表中的ID",verbose_name="对应权限种类表中的ID",db_index=True)
    permission_type = models.CharField(max_length=64,null=False,help_text="权限类型",verbose_name="权限类型",db_index=True)    


class RolePermissionShip(BaseModel):
    class Meta:
        db_table = "rbac_role_permission"
        verbose_name = "rbac_角色权限关联表"
        verbose_name_plural = "rbac_角色权限关联表"   
        unique_together = ('role_id', 'permission_id') 
    
    role_id = models.IntegerField(null=False,help_text="角色ID",verbose_name="角色ID",db_index=True)
    permission_id = models.IntegerField(null=False,help_text="权限ID",verbose_name="权限ID",db_index=True)      

# 以下是不同种类的权限，直接增加一个字段合并到权限表？

class Menu(BaseModel):
    # 菜单，包括一级菜单/二级菜单/三级菜单
    class Meta:
        db_table = "rbac_menu"
        verbose_name = "rbac_菜单"
        verbose_name_plural = "rbac_菜单"

    menu_name = models.CharField(max_length=128,null=False,help_text="菜单名称",verbose_name="菜单名称")
    menu_url = models.CharField(max_length=128,null=False,help_text="菜单url",verbose_name="菜单url",unique=True)
    menu_icon = models.CharField(max_length=128,null=True,blank=True,help_text="菜单对应的vue-icon",verbose_name="菜单对应的Vue-icon")
    menu_type = models.SmallIntegerField(null=False,default=0,help_text="菜单类型:0菜单 1按钮",verbose_name="菜单类型:0菜单 1按钮")
    menu_view_path = models.CharField(max_length=128,null=False,help_text="菜单对应的page路径",verbose_name="菜单对应的page路径")
    menu_route_name = models.CharField(max_length=128,null=False,help_text="路由名称",verbose_name="路由名称")
    p_id = models.ForeignKey("Menu",null=True,help_text="父级菜单",verbose_name="父级菜单",on_delete=models.CASCADE)
    # redirect = models.CharField(max_length=128,null=True,help_text="重定向到路由名称",verbose_name="重定向到路由名称")

# class MenuPermissionShip(BaseModel):
#     # 菜单权限关联到中间权限表
#     class Meta:
#         db_table = "rbac_permission_menu"
#         verbose_name = "rbac_菜单权限关联表"
#         verbose_name_plural = "rbac_菜单权限关联表"    
#         unique_together = ('menu_id', 'permission_id') 
    
#     menu_id = models.IntegerField(null=False,help_text="菜单id",verbose_name="菜单id")
#     permission_id = models.IntegerField(null=False,help_text="对应的权限id",verbose_name="对应的权限id")


class ModelOperation(BaseModel):
    # 表的操作权限，这里对应的DJANGO的model权限
    class Meta:
        db_table = "rbac_model_operation"
        verbose_name = "rbac_表操作权限"
        verbose_name_plural = "rbac_表操作权限"
        unique_together = ('op_name', 'op_model_name')

    app_label = models.CharField(max_length=128,default="undefined",null=False,help_text="表所对应的app名称",verbose_name="表所对应的app名称")
    op_name = models.CharField(max_length=128,null=False,help_text="操作名称",verbose_name="操作名称")
    # op_model = models.IntegerField(null=False,help_text="操作的表",verbose_name="操作的表")
    op_model_name = models.CharField(max_length=128,null=False,help_text="操作表的名称",verbose_name="操作表的名称")
    description = models.TextField(null=True,blank=True,help_text="操作的权限的描述",verbose_name="操作的权限的描述")
    p_id = models.ForeignKey("ModelOperation",null=True,help_text="父操作ID",verbose_name="父操作ID",on_delete=models.CASCADE)



# class OperationPermissionShip(BaseModel):
#     class Meta:
#         db_table = "rbac_operation_permission"
#         verbose_name = "rbac_表操作权限关联表"
#         verbose_name_plural = "rbac_表操作权限关联表"
#         unique_together = ('op_id', 'permission_id') 

#     op_id = models.IntegerField(null=False,help_text="操作id",verbose_name="操作id")
#     permission_id = models.IntegerField(null=False,help_text="对应的权限id",verbose_name="对应的权限id")