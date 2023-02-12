from rest_framework.viewsets import ModelViewSet
from thirdApis.models import ChatGPTConversation,ChatGPTMessage,User
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from thirdApis.chatGPT.serializers import ChatGPTConversationSerializer,ChatGPTMessageSerializer
from utils.http_ import HTTPResponse
from rest_framework import status

class ChatGPTConversationViewsSet(ModelViewSet):
    queryset = ChatGPTConversation.objects.all()    
    serializer_class = ChatGPTConversationSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]


    def retrieve(self, request, *args, **kwargs):
        return HTTPResponse(
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )


    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    
    def destroy(self, request,pk=None):
        super().destroy(request, pk)
        return HTTPResponse(
            message="删除成功!"
        )
    

    def create(self, request, *args, **kwargs):
        serializer = ChatGPTConversationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return HTTPResponse(serializer.data)
    
    def update(self, request, *args, **kwargs):
        res = super().update(request, *args, **kwargs)
        return HTTPResponse(data=res.data)


class ChatGPTMessageViewSet(ModelViewSet):
    queryset=ChatGPTMessage.objects.all()
    serializer_class = ChatGPTMessageSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        res = super().create(request, *args, **kwargs)
        return HTTPResponse(data=res.data)

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        return HTTPResponse(
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )

    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
    
    def update(self, request, *args, **kwargs):
        return HTTPResponse(
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )