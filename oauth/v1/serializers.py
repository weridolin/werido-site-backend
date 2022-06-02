from rest_framework.serializers import ModelSerializer
from oauth.models import OauthModel

class ApplicationSerializer(ModelSerializer):
    class Meta:
        model = OauthModel
        fields = '__all__'


    def validate(self, attrs):
        return super().validate(attrs)

    def save(self, **kwargs):
        return super().save(**kwargs)

    def create(self, validated_data):
        return super().create(validated_data)