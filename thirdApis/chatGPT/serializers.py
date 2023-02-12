from core.base import BaseSerializer
from thirdApis.models import ChatGPTMessage,ChatGPTConversation
from authentication.v1.serializers import UserSerializer

class ChatGPTConversationSerializer(BaseSerializer):
    user = UserSerializer(required=False)

    class Meta:
        model = ChatGPTConversation
        fields = "__all__"
        depth=1

class ChatGPTMessageSerializer(BaseSerializer):

    class Meta:
        model = ChatGPTMessage
        fields = "__all__"
        depth=1