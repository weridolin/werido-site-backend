from rest_framework.viewsets import ModelViewSet
from rest_framework import parsers
from wechat.models import WechatMessage
from wechat.v1.seriazliers import WechatMessageSerializer
from rest_framework_xml.parsers import XMLParser
from rest_framework_xml.renderers import XMLRenderer


class PublicCountMessageApis(ModelViewSet):

    model = WechatMessage
    parser_classes=[XMLParser]
    serializer_class =WechatMessageSerializer
    renderer_classes=[XMLRenderer]


    def create(self, request, *args, **kwargs):
        print(">>> get message",request.data)
        return super().create(request, *args, **kwargs)