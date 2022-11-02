from django.shortcuts import render
from rbac.models import ModelOperation,Menu,Permissions,OperationPermissionShip

# Create your views here.

PERMISSION_ORM_REF = {
    "model_op":ModelOperation,
    "menu":Menu,
}

ORM_PERMISSION_REF = {
    ModelOperation:"model_op",
    Menu:"menu"
}


def add_permission(orm,**kwargs):
    op_permission,is_exits = orm.objects.update_or_create(**kwargs)
    if not is_exits:
        permission = Permissions.objects.create(permission_type=ORM_PERMISSION_REF.get(orm)) 
        permission.save()
        OperationPermissionShip.objects.update_or_create(op_id=op_permission.id,permission_id=permission.id)

