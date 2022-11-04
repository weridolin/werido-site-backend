from django.shortcuts import render
from rbac.models import ModelOperation,Menu,Permissions,OperationPermissionShip
from rest_framework.permissions import DjangoModelPermissions
from rbac.permission import ORM_PERMISSION_REF,PERMISSION_ORM_REF

# Create your views here.



def add_permission(orm,**kwargs):
    op_permission,is_exits = orm.objects.update_or_create(**kwargs)
    if not is_exits:
        permission = Permissions.objects.create(permission_type=ORM_PERMISSION_REF.get(orm)) 
        permission.save()
        OperationPermissionShip.objects.update_or_create(op_id=op_permission.id,permission_id=permission.id)

