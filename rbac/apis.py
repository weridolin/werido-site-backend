from django.shortcuts import render
from rbac.models import ModelOperation,Menu,Permissions
from rest_framework.permissions import DjangoModelPermissions
# from rbac.permission import ORM_PERMISSION_REF,PERMISSION_ORM_REF

# Create your views here.



def add_model_op_permission(app_label=None,op_name=None,op_model_name=None,description=None,p_id=None):
    op,is_exits = ModelOperation.objects.update_or_create(op_model_name=op_model_name,op_name=op_name,app_label=app_label,defaults={
        "description":description,
        "p_id":p_id,
    })
    if not is_exits:
        permission,_ = Permissions.objects.update_or_create(permission_type="model_op",permission_id=op.id) 
        permission.save()



def add_menu(menu_name,menu_url,menu_icon,menu_type,menu_view_path,menu_route_name,p_id=None):
    menu,is_exits = Menu.objects.update_or_create(menu_url=menu_url,defaults={
        "menu_name":menu_name,
        "menu_icon":menu_icon,
        "menu_type":menu_type,
        "menu_view_path":menu_view_path,
        "p_id":p_id,
        "menu_route_name":menu_route_name
    })
    menu.save()
    # 往permission_menu表
    if not is_exits:
        permission,_ = Permissions.objects.update_or_create(permission_type="menu",permission_id=menu.id) 
        permission.save()        
    return menu


from rest_framework.views import APIView
from utils.http_ import HTTPResponse
from rbac.models import Menu
from rbac.serializers import MenuSerializer
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication

class MenuApis(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes=[]

    def get(self,request,pk=None):
        if not pk:
            menus=Menu.objects.all()
            return HTTPResponse(
                data=MenuSerializer(menus,many=True).data
            )
        else:
            try:
                menus=Menu.objects.get(id=pk)
                return HTTPResponse(
                    data=MenuSerializer(menus).data
                )                
            except Menu.DoesNotExist:
                return HTTPResponse(
                    status=status.HTTP_404_NOT_FOUND,
                    message=f"can not find menu(id={pk})"
                )

