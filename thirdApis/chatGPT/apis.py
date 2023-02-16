from rest_framework.viewsets import ModelViewSet
from thirdApis.models import ChatGPTConversation,ChatGPTMessage,User
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from thirdApis.chatGPT.serializers import ChatGPTConversationSerializer,ChatGPTMessageSerializer
from utils.http_ import HTTPResponse
from rest_framework import status
from core.base import PageNumberPaginationWrapper
import django_filters
class ChatGPTPagination(PageNumberPaginationWrapper):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1000


class ChatGPTConversationViewsSet(ModelViewSet):
    queryset = ChatGPTConversation.objects.all()    
    serializer_class = ChatGPTConversationSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    pagination_class = ChatGPTPagination


    def retrieve(self, request, *args, **kwargs):
        return HTTPResponse(
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )


    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    
    def destroy(self, request,pk=None):
        if pk:
            super().destroy(request, pk)
        else:
            self.queryset.delete()
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

class ChatGPTMessageFilterSet(django_filters.FilterSet):
    #  省份信息筛选字段
    # title 为 request get的字段

    conversation_uuid = django_filters.CharFilter(
        lookup_expr="iexact", field_name="conversation_uuid")

    class Meta:
        model = ChatGPTMessage
        fields = ["conversation_uuid"]


class ChatGPTMessageViewSet(ModelViewSet):
    queryset=ChatGPTMessage.objects.all()
    serializer_class = ChatGPTMessageSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    pagination_class = ChatGPTPagination
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_class = ChatGPTMessageFilterSet

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