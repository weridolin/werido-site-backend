from rest_framework.viewsets import ModelViewSet
from rest_framework import parsers
from wechat.models import WechatMessage
from wechat.v1.seriazliers import WechatMessageSerializer
from rest_framework_xml.parsers import XMLParser
from rest_framework_xml.renderers import XMLRenderer
import hashlib
import os
from utils.http_ import HTTPResponse
from rest_framework import status

class PublicCountMessageApis(ModelViewSet):

    model = WechatMessage
    parser_classes=[XMLParser]
    serializer_class =WechatMessageSerializer
    renderer_classes=[XMLRenderer]
    queryset = WechatMessage

    def create(self, request, *args, **kwargs):
        print(">>> get wechat message",request.data)
        return super().create(request, *args, **kwargs)
    
    def retrieve(self, request, *args, **kwargs):
        try:
            data = request.data
            signature = data.get("signature")
            timestamp = data.get("timestamp")
            nonce = data.get("nonce")
            echostr = data.get("echostr")
            token = os.environ.get("WECHAT_URL_TOKEN")

            list_ = [token, timestamp, nonce]
            list_.sort()
            sha1 = hashlib.sha1()
            map(sha1.update, list_)
            hashcode = sha1.hexdigest()

            if hashcode == signature:
                return HTTPResponse(
                    message=echostr
                )
            else:
                return HTTPResponse(
                    status=status.HTTP_400_BAD_REQUEST,
                    message=f"hashcode不等于signature"
                )
        except Exception as exc:
            return HTTPResponse(
                status=status.HTTP_400_BAD_REQUEST,
                message=str(exc)
            )