from rest_framework.permissions import BasePermission
from rbac.models import RolePermissionShip,UserRoleShip,ModelOperation,Role,GroupRoleShip,Group,UserGroupShip,Permissions,Menu,MenuPermissionShip,OperationPermissionShip
from django_redis import get_redis_connection
from redis.client import Redis
from rest_framework import exceptions
from rest_framework_simplejwt.tokens import RefreshToken
from core import settings
from rest_framework_simplejwt.backends import TokenBackend
from django.contrib.auth.models import User
from utils.redis_keys import UserPermission
import json


PERMISSION_ORM_REF = {
    "model_op":(ModelOperation,OperationPermissionShip),
    "menu":(Menu,MenuPermissionShip)
}

ORM_PERMISSION_REF = {
    ModelOperation:"model_op",
    Menu:"menu"
}


class RbacModelPermission(BasePermission):
    # 参考DJANGO MODEL PERMISSION
    perms_map = {
        'GET': [], ##  todo ['%(app_label)s.view_%(model_name)s'],?
        'OPTIONS': [],
        'HEAD': [],
        'POST': ['%(app_label)s.post_%(model_name)s'],
        'PUT': ['%(app_label)s.update_%(model_name)s'],
        'PATCH': ['%(app_label)s.update_%(model_name)s'],
        'DELETE': ['%(app_label)s.delete_%(model_name)s'],
    }

    def has_permission(self, request, view):
        if hasattr(view,"queryset"):
            orm = view.queryset.model
        elif hasattr(view,"orm"):
            orm = view.orm
        else:
            raise AttributeError("view must have queryset or orm attribute")
    
        if request.method not in self.perms_map:
            raise exceptions.MethodNotAllowed(request.method)
        
        if request.user.is_superuser:
            return True

        kwargs = {
            'app_label': orm._meta.app_label,
            'model_name': orm._meta.model_name
        }
        perm_required = [perm % kwargs for perm in self.perms_map[request.method]]

        user_perms = self._get_perms_from_token(request)    

        if "model_op" not in user_perms:
            return False

        
        print("user perms",user_perms,"required perms",perm_required)

        for perm in perm_required:
            if  perm not in user_perms["model_op"]:
                return False 
        return True


    def _get_perms_from_token(self,request):
        token = request.META.get('HTTP_AUTHORIZATION', " ").split(' ')[1]
        decode_at = TokenBackend(algorithm=settings.SIMPLE_JWT.get("ALGORITHM")).decode(token,verify=False)
        roles,uuid = decode_at["roles"],decode_at["uuid"]
        conn:Redis = get_redis_connection("default") # return redis client:<redis.client.Redis>
        perms = conn.get(UserPermission.permission_key(user=request.user,uuid=uuid))
        if perms:
            return  json.loads(perms)
        _,_,perms = get_user_perms(user=request.user)
        return perms

def get_user_roles(user):
    user_roles = UserRoleShip.objects.filter(user_id =user.id).all()
    roles = Role.objects.filter(id__in=[role.role_id for role in user_roles]).all()
    return roles

def get_user_groups(user):
    user_groups_ids= UserGroupShip.objects.filter(user_id =user.id).all()
    groups = Group.objects.filter(id__in=user_groups_ids).all()
    return groups

def get_roles_perms(roles):
    perms = dict()
    if roles:
        role_ids =[role.id for role in roles]
        role_perms = RolePermissionShip.objects.filter(role_id__in=role_ids).all()
        if role_perms:
            # 先获取操作的权限
            perms_refs = Permissions.objects.filter(id__in=[role_perm.permission_id for role_perm in role_perms],permission_type="model_op").all()
            perms_ships = OperationPermissionShip.objects.filter(permission_id__in=[perms_ref.id for perms_ref in perms_refs]).all()
            real_perms = ModelOperation.objects.filter(id__in=[perms_ship.op_id for perms_ship in perms_ships]).all()
            perms.update({
                "model_op": [f'{op_perm.app_label}.{op_perm.op_name}_{op_perm.op_model_name}' for op_perm in real_perms]
            })
            # 在获取表单权限

            # print("op_perms",[perm.permission_id for perm in perms])
            # return [f'{op_perm.app_label}.{op_perm.op_name}_{op_perm.op_model_name}' for op_perm in op_perms]
    return perms


def get_group_perms(groups):
    perms = dict()
    if groups:
        group_ids = [group.id for group in groups]
        roles = GroupRoleShip.objects.filter(group_id__in=group_ids).all()
        if roles:
            return get_roles_perms(roles)
    return perms

def get_user_perms(user):
    roles = get_user_roles(user=user)
    role_perms = get_roles_perms(roles)
    groups = get_user_groups(user)
    # groups_perms = get_group_perms(groups)

    # for  

    # user_perms = set(role_perms)
    return roles,groups,role_perms
        
