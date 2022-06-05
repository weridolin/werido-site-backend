from rest_framework.serializers import ModelSerializer,Serializer
from rest_framework.serializers import (
    BooleanField,
    CharField,

    )
from oauth.models import OauthApplicationModel
from authentication.v1.serializers import UserSerializer
class ApplicationSerializer(ModelSerializer):
    class Meta:
        model = OauthApplicationModel
        fields = '__all__'


    def validate(self, attrs):
        return super().validate(attrs)

    def save(self, **kwargs):
        return super().save(**kwargs)

    def create(self, validated_data):
        return super().create(validated_data)

# class Application
class ApplicationBriefSerializer(ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = OauthApplicationModel
        fields = ["client_id","user","redirect_uris","authorization_grant_type","name"]
        depth = 1 

class AuthorizationSerializer(Serializer):
    allow = BooleanField(required=False)
    redirect_uri = CharField(required=True)
    scope = CharField(required=True)
    nonce = CharField(required=False)
    client_id = CharField(required=True)
    state = CharField(required=False)
    response_type = CharField(required=True)
    code_challenge = CharField(required=False)
    code_challenge_method = CharField(required=False)
    claims = CharField(required=False)