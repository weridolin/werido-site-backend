import django_filters
from django_filters.rest_framework.backends import DjangoFilterBackend
from core.base import OrderingFilterWrapper
from core.base import PageNumberPaginationWrapper
from rest_framework.viewsets import ModelViewSet
from rest_framework.pagination import PageNumberPagination
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import status
from rbac.serializers import MenuSerializer
from rbac.models import Menu
from utils.http_ import HTTPResponse
from rest_framework.views import APIView
from rbac.models import ModelOperation, Menu, Permissions
from rest_framework.permissions import DjangoModelPermissions
from rbac.permission import format_menu
from rest_framework.generics import ListAPIView
# Create your views here.


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
    # title 为 request get的字段
    menu_name = django_filters.CharFilter(
        lookup_expr="icontains", field_name="menu_name")
    menu_type = django_filters.CharFilter(
        lookup_expr="iexact", field_name="menu_type")
    # tags = django_filters.CharFilter(lookup_expr="icontains", field_name = "tags__name")
    created = django_filters.DateTimeFromToRangeFilter(field_name="created")
    class Meta:
        model = Menu
        fields = ["menu_name", "menu_type","created"]


class MenuApis(ModelViewSet):

    authentication_classes = [JWTAuthentication]
    permission_classes = []
    pagination_class = MenuPagination
    filter_backends = [OrderingFilterWrapper, DjangoFilterBackend]
    filterset_class = MenuFilterSet
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer

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
            serializer.save(p_id=p_id)
        else:
            serializer.save(p_id=None)

        return HTTPResponse(
            message="create menu success!"
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
            /menu/{pk}   put
            删除菜单
        """
        if not pk:
            return HTTPResponse(
                status=status.HTTP_400_BAD_REQUEST,
                message="菜单ID不能为空"
            )
        else:
            try:
                menu = Menu.objects.get(id=pk)
                menu.delete()
                return HTTPResponse(
                    message="删除成功"
                )
            except Menu.DoesNotExist:
                return HTTPResponse(
                    status=status.HTTP_404_NOT_FOUND,
                    message="找不到菜单ID"
                )
