from rest_framework.viewsets import GenericViewSet
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAdminUser
from covid19.models import Province,Country,City
from covid19.v1.serializers import ProvinceInfoSerializer,CityInfoSerializer,CountryInfoSerializer
from core.base import HTTPResponse
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
import django_filters


class CovidInfoFilterSet(django_filters.FilterSet):
    # title 为 request get的字段
    menu_name = django_filters.CharFilter(
        lookup_expr="icontains", field_name="menu_name")
    menu_type = django_filters.CharFilter(
        lookup_expr="iexact", field_name="menu_type")
    # tags = django_filters.CharFilter(lookup_expr="icontains", field_name = "tags__name")
    created = django_filters.DateTimeFromToRangeFilter(field_name="created") ## before_created / after_created
    class Meta:
        model = Province
        fields = ["menu_name", "menu_type","created"]

class CovidApis(ModelViewSet):
    
    authentication_classes=[JWTAuthentication]
    # permission_classes=[]
    
    
    def get_queryset(self):
        _type = self.request.data.get("type")
        if _type=="city":
            self.queryset=City.objects.all()
        elif _type=="province":
            self.queryset=City.objects.all()
        elif _type=="country":
            self.queryset=City.objects.all()
        else:
            return HTTPResponse(
                code=-1,
                status=status.HTTP_400_BAD_REQUEST,
                message="type error only support 'city'|'province'|'country'"
            )
        # return super().get_queryset()
        return self.queryset
    
    def get_serializer_class(self):
        _type = self.request.data.get("type")
        if _type=="city":
            self.serializer_class=CityInfoSerializer
        elif _type=="province":
            self.serializer_class=ProvinceInfoSerializer
        elif _type=="country":
            self.serializer_class=CountryInfoSerializer
        return self.serializer_class


    # def get_object(self):
    #     return super().get_object()
    
    def _get_province_info(self,request):
        records = Province.objects.all()
        data = ProvinceInfoSerializer(records,many=True).data


    def _get_country_info(self,request):
        ...


    # @action(detail=True, methods=['post'])
    # def update_data(self, request, pk=None):
    #     ...
    
    def list(self, request, *args, **kwargs):
        
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        # print(serializer,queryset)
        return HTTPResponse(serializer.data)

    def create(self, request, *args, **kwargs):
        
        return super().create(request, *args, **kwargs)
    
    def retrieve(self, request, *args, **kwargs):
        return HTTPResponse(code=-1,status=status.HTTP_405_METHOD_NOT_ALLOWED,message="请求方法不允许")
    

    def update(self, request, *args, **kwargs):
        return HTTPResponse(code=-1,status=status.HTTP_405_METHOD_NOT_ALLOWED,message="请求方法不允许")

    
    def destroy(self, request, *args, **kwargs):
        return HTTPResponse(code=-1,status=status.HTTP_405_METHOD_NOT_ALLOWED,message="请求方法不允许")


    