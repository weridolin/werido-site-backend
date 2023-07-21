import django_filters
from django_filters.rest_framework.backends import DjangoFilterBackend
from core.base import OrderingFilterWrapper
from core.base import PageNumberPaginationWrapper
from rest_framework.viewsets import ModelViewSet,ViewSet,GenericViewSet
from rest_framework import mixins
from rest_framework.pagination import PageNumberPagination
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import status
from rbac.serializers import MenuSerializer, RoleSerializer,ModelAccessSerializer
from rbac.models import Menu
from utils.http_ import HTTPResponse
from rest_framework.views import APIView
from rbac.models import ModelOperation, Menu, Permissions, Role,UserRoleShip,RolePermissionShip
from rest_framework.permissions import DjangoModelPermissions
from rbac.permission import format_menu
from rest_framework.generics import ListAPIView,DestroyAPIView,GenericAPIView,CreateAPIView,UpdateAPIView
from rest_framework.renderers import JSONRenderer, StaticHTMLRenderer
from rest_framework.parsers import JSONParser, MultiPartParser
from rest_framework.decorators import action
from rest_framework import permissions
from rbac.models import RolePermissionShip

def add_model_op_permission(app_label=None, op_name=None, op_model_name=None, description=None, p_id=None):
    op, is_exits = ModelOperation.objects.update_or_create(op_model_name=op_model_name, op_name=op_name, app_label=app_label, defaults={
        "description": description,
        "p_id": p_id,
    })
    if not is_exits:
        permission, _ = Permissions.objects.update_or_create(
            permission_type="model_op", permission_id=op.id)
        permission.save()


def add_menu(menu_name, menu_url, menu_icon, menu_type, menu_view_path, menu_route_name, p_id=None):
    menu, is_exits = Menu.objects.update_or_create(menu_url=menu_url, defaults={
        "menu_name": menu_name,
        "menu_icon": menu_icon,
        "menu_type": menu_type,
        "menu_view_path": menu_view_path,
        "p_id": p_id,
        "menu_route_name": menu_route_name
    })
    menu.save()
    # 往permission_menu表
    if not is_exits:
        permission, _ = Permissions.objects.update_or_create(
            permission_type="menu", permission_id=menu.id)
        permission.save()
    return menu


class MenuPagination(PageNumberPaginationWrapper):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1000


class MenuFilterSet(django_filters.FilterSet):
    #  省份信息筛选字段
    # title 为 request get的字段
    menu_name = django_filters.CharFilter(
        lookup_expr="icontains", field_name="menu_name")
    menu_type = django_filters.CharFilter(
        lookup_expr="iexact", field_name="menu_type")
    # tags = django_filters.CharFilter(lookup_expr="icontains", field_name = "tags__name")
    created = django_filters.DateTimeFromToRangeFilter(
        field_name="created")  # before_created / after_created

    class Meta:
        model = Menu
        fields = ["menu_name", "menu_type", "created"]

# class CovidCountryInfoFilterSet(django_filters.FilterSet):
#     #  省份信息
#     ...


class MenuApis(GenericViewSet):

    authentication_classes = [JWTAuthentication]
    permission_classes = []  # todo

    # 分页
    pagination_class = MenuPagination

    filter_backends = [OrderingFilterWrapper, DjangoFilterBackend]
    filterset_class = MenuFilterSet
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer

    # 只允许返回JSON，加了这个限制,如果请求头限制了accept的类型不包含JSON，则返回406
    renderer_classes = [JSONRenderer]

    # 只能处理content-type为application/json的request.body，
    # 加了这个限制,如果请求头content-type不为JSON，则返回415
    # 默认为JSONParser
    parser_classes = [JSONParser, MultiPartParser]

    # search_fields = ['menu_name', 'menu_type']

    def list(self, request, *args, **kwargs):

        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return HTTPResponse(
            data=serializer.data
        )

    def create(self, request):
        """
            /menu/   post
            创建一个菜单
        """
        print(">>> 创建菜单",request.data)
        p_id = request.data.pop("p_id", None)
        serializer = MenuSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if p_id:
            try:
                p_id = Menu.objects.get(id=p_id)
            except Menu.DoesNotExist:
                return HTTPResponse(
                    status=status.HTTP_404_NOT_FOUND,
                    message="找不到对应的父级菜单"
                )
        try:
            with transaction.atomic():     
                # 菜单表创建一个菜单  
                serializer.save(p_id=p_id)
                return HTTPResponse(
                    message="create menu success!"
                )
                
        except Exception as exc:
            return HTTPResponse(
                message=f"创建菜单失败:{exc}"
            )

    def retrieve(self, request, pk=None):
        """
            /menu/{pk}    get
            根据ID获取菜单
        """
        if not pk:
            # menus=Menu.objects.all()
            return HTTPResponse(
                status=status.HTTP_404_NOT_FOUND,
                message="菜单ID不能为空."
            )
        else:
            try:
                menus = Menu.objects.all()
                target = Menu.objects.get(id=pk)
                menus_serializer = MenuSerializer(menus, many=True)
                target_serializer = MenuSerializer(target)
                if menus and target:
                    res = target_serializer.data
                    res["children"] = format_menu(
                        menus_serializer.data, parent=target.id, cache=list())
                    return HTTPResponse(
                        data=res
                    )
            except Menu.DoesNotExist:
                return HTTPResponse(
                    status=status.HTTP_404_NOT_FOUND,
                    message=f"can not find menu(id={pk})"
                )

    def update(self, request, pk=None):
        """
            /menu/{pk}   put
            更新菜单
        """
        if not pk:
            return HTTPResponse(
                status=status.HTTP_400_BAD_REQUEST,
                message="菜单ID不能为空!"
            )
        else:
            try:
                p_id = request.data.pop("p_id", None)
                if p_id:
                    p_id = Menu.objects.get(id=p_id)
                menu = Menu.objects.get(id=pk)
                serializer = MenuSerializer(instance=menu, data=request.data)
                serializer.is_valid(raise_exception=True)
                serializer.save(p_id=p_id)
                return HTTPResponse(
                    message="菜单更新成功"
                )
            except Menu.DoesNotExist:
                return HTTPResponse(
                    status=status.HTTP_404_NOT_FOUND,
                    message="找不到菜单ID"
                )

    def destroy(self, request, pk=None):
        """
            /menu/  delete
            删除菜单
        """
        menu_ids= request.data.get("menu_ids",[])
        try:
            with transaction.atomic():
                # 1删除对应的菜单
                menus = Menu.objects.filter(id__in=menu_ids).all()
                menus.delete()

                # 2 删除对应的permission表
                perms_ref =Permissions.objects.filter(permission_id__in=menu_ids).all()
                perms_ref.delete()

                # 3 删除角色-权限表
                role_perms_ref = RolePermissionShip.objects.filter(permission_id__in=[perm.id for perm in perms_ref])
                role_perms_ref.delete()

                return HTTPResponse(
                    message=f"删除菜单成功"
                )
        except Exception as exc:
            return HTTPResponse(
                code=-1,
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                message=f"删除菜单失败:{exc}"
            )    


class ModelOperationFilterSet(django_filters.FilterSet):
    #  表操作权限
    # title 为 request get的字段
    op_model_name = django_filters.CharFilter(
        lookup_expr="icontains", field_name="op_model_name")

    created = django_filters.DateTimeFromToRangeFilter(
        field_name="created")  # before_created / after_created

    class Meta:
        model = Menu
        fields = ["op_model_name", "created"]


class ModelOperationApis(GenericViewSet):

    queryset = ModelOperation.objects.all()
    permission_classes=[permissions.IsAdminUser]
    authentication_classes=[JWTAuthentication]
    serializer_class=ModelAccessSerializer
    
    def list(self, request, *args, **kwargs):
        res= super().list(request, *args, **kwargs)
        return HTTPResponse(
            res.data
        )


    def destroy(self, request, *args, **kwargs):
        perm_ids = request.data.get("permission_ids",[])
        print(">>>delete permission",perm_ids)
        try: ## 尽量避免在with里面使用 try-catch
            with transaction.atomic():
                ## 创建事务保存点
                # point = transaction.savepoint()
                ## 1.删除model op 表对应的操作权限
                perms = ModelOperation.objects.filter(id__in=perm_ids).all()
                perms.delete()
                ## 2.删除对应的permission表中的记录
                perms_ref = Permissions.objects.filter(permission_id__in=perm_ids).all()
                perms_ref.delete()
                ## 3.删除角色-权限表
                perms_role_ids = RolePermissionShip.objects.filter(permission_id__in=perm_ids).all()
                perms_role_ids.delete()
                # transaction.savepoint_commit(point)
                return HTTPResponse(
                    message="删除成功!"
                )
        except Exception as exc:
            # transaction.savepoint_rollback(point)
            return HTTPResponse(
                code=-1,
                message=f"删除权限失败:{exc}",
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class RoleFilterSet(django_filters.FilterSet):
    #  表操作权限
    # title 为 request get的字段
    role_name = django_filters.CharFilter(
        lookup_expr="icontains", field_name="role_name")

    created = django_filters.DateTimeFromToRangeFilter(
        field_name="created")  # before_created / after_created

    class Meta:
        model = Role
        fields = ["role_name", "created"]


class RolePagination(PageNumberPaginationWrapper):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

from django.db import transaction

class RoleApis(GenericViewSet,mixins.ListModelMixin,mixins.UpdateModelMixin):
    queryset = Role.objects.all()
    authentication_classes = [JWTAuthentication]
    permission_classes=[permissions.IsAdminUser]
    serializer_class = RoleSerializer

    # 返回格式,要跟request header里面的 accept 字段对上
    renderer_classes = [JSONRenderer]

    # 筛选
    filter_backends = [OrderingFilterWrapper, DjangoFilterBackend]
    filterset_class = RoleFilterSet    

    # 分页,已经在分页器的响应里面统一了返回格式
    pagination_class=RolePagination


    def create(self, request, *args, **kwargs):
        """
            创建新角色
        """
        role_name = request.data.get("role_name")
        if not role_name:
            return HTTPResponse(
                status=status.HTTP_400_BAD_REQUEST,
                message="角色姓名不能为空",
                app_code="rbac"

            )
        else:
            if Role.objects.filter(role_name=role_name).exists():
                return HTTPResponse(
                    status=status.HTTP_400_BAD_REQUEST,
                    message="该角色已经存在",
                    app_code="rbac"

                )
            
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return HTTPResponse(
            message=f"创建角色[{role_name}]成功!",
            app_code="rbac"
        )


    def destroy(self, request, *args, **kwargs):
        """
            删除角色
        """
        role_ids= request.data.get("role_ids",[])
        print(">>> delete roles",role_ids)
        try: # 避免在atomic里面使用try-catch
            # 事务操作
            with transaction.atomic():
                ## 1.删除对应的角色
                roles = Role.objects.filter(id__in=role_ids).all()
                roles.delete()
                ## 2.删除对应的权限
                # user_role_ids = UserRoleShip.objects.filter(role_id__in=role_ids).all()
                perms_role_ids = RolePermissionShip.objects.filter(role_id__in=role_ids).all()
                perms_role_ids.delete()
                ## 3.删除用户-角色表
                user_role_ids = UserRoleShip.objects.filter(role_id__in=role_ids).all()
                user_role_ids.delete()
                return HTTPResponse(
                    message="删除成功!"
                )
        except Exception as exc:
            return HTTPResponse(
                code=-1,
                message=f"删除角色失败:{exc}",
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


    @action(
        methods=["POST"],  
        authentication_classes=[JWTAuthentication],
        permission_classes=[permissions.IsAdminUser],
        detail=False,
        url_name="rbac-set-role-perms",
        url_path="setPerms")
    def set_permission(self,request):
        perm_ids,role_id= request.data.get("perm_ids"),request.data.get("role_id")
        # print(">>>",perm_ids,role_id)
        if not role_id:
            return HTTPResponse(
                status=status.HTTP_400_BAD_REQUEST,
                message="请先选择角色"
            )
        for perm_id in perm_ids:
            RolePermissionShip.objects.update_or_create(
                role_id=role_id,
                permission_id=perm_id
            )
        return HTTPResponse(
            message="为用户设置权限成功!",
            app_code="rbac"
        )
    
# class PermissionApis():
#     queryset=Permissions.objects.all()
#     authentication_classes=[JWTAuthentication]
#     permission_classes=[permissions.IsAdminUser]



#     def list(self, request, *args, **kwargs):
#         return super().list(request, *args, **kwargs)