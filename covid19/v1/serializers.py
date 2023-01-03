# from core.base import BaseSerializer

from covid19.models import Country,City,Policy,Province
from rest_framework import serializers

class BaseSerializer(serializers.ModelSerializer):
    created = serializers.DateField(
        format="%Y-%m-%d", read_only=True)
    updated = serializers.DateField(
        format="%Y-%m-%d", read_only=True)    



class CountryInfoSerializer(BaseSerializer):
    class Meta:
        model=Country
        fields = "__all__"

class CityInfoSerializer(BaseSerializer):
    class Meta:
        model=City
        fields = "__all__"

class ProvinceInfoSerializer(BaseSerializer):
    class Meta:
        model=Province
        fields="__all__"

