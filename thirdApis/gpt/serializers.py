from core.base import BaseSerializer
from thirdApis.models import GptMessage,GptConversation
# from authentication.v1.serializers import UserSerializer
from rest_framework import serializers

class GptConversationSerializer(BaseSerializer):
    # user = UserSerializer(required=False)

    class Meta:
        model = GptConversation
        fields = "__all__"
        # depth=1

class GptMessageSerializer(BaseSerializer):
    # query_content =  serializers.SerializerMethodField(method_name="get_query_content")
    # reply_content = serializers.SerializerMethodField(method_name="get_reply_content")
    class Meta:
        model = GptMessage
        fields = "__all__"
        depth=1

    # def get_query_content(self,object:GptMessage):
    #     if object.role==0:
    #         return object.content
    #     return ""
    

    # def get_reply_content(self,object):
    #     if object.role==1:
    #         return object.content
    #     return ""
            