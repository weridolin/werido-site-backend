from rest_framework.viewsets import ModelViewSet
from thirdApis.models import GptConversation,GptMessage
from thirdApis.gpt.serializers import GptConversationSerializer,GptMessageSerializer
from utils.http_ import HTTPResponse
from rest_framework import status
from core.base import PageNumberPaginationWrapper
import django_filters
from thirdApis.gpt.celery_tasks import clear_message
from rest_framework.decorators import action
import uuid
from  utils.jwt import generate_jwt_token
import datetime
from core import settings
from authenticationV1 import V1Authentication
from utils.rabbitmq import public_message
import json
import logging,asyncio
from thirdApis.gpt.ali.request import HttpRequest as AliHttpRequest,HttpMixins
from thirdApis.gpt.manager import get_manager

# logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class GptPagination(PageNumberPaginationWrapper):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1000



class GptConversationViewsSet(ModelViewSet):
    """
        1个conversation对应多个message,对应单个websocketID
    """
    # queryset = GptConversation.objects.all()    
    serializer_class = GptConversationSerializer
    # permission_classes = [IsAuthenticated]
    pagination_class = GptPagination
    authentication_classes = [V1Authentication]

    def get_queryset(self):
        query_set =  GptConversation.objects.all()
        if self.request.user:
            return query_set.filter(user_id=self.request.user,deleted=False)
        else:
            return query_set.filter(deleted=False)

    def retrieve(self, request, *args, **kwargs):
        return HTTPResponse(
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )


    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    
    def destroy(self, request,pk=None):
        if pk!="all":
            print("delete all")
            # super().destroy(request, pk)
            # clear_message.delay(conversation_id=pk)
            GptConversation.objects.filter(uuid=pk).update(deleted=True)
        else:
            GptConversation.objects.filter(user_id=request.user).update(deleted=True)
        return HTTPResponse(
            message="删除成功!"
        )

    def create(self, request, *args, **kwargs):
        user_id = int(request.user)
        request.data.update({
            "user_id":user_id
        })
        serializer = GptConversationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user_id=request.user)
        return HTTPResponse(serializer.data)
    
    def update(self, request, *args, **kwargs):
        res = super().update(request, *args, **kwargs)
        return HTTPResponse(data=res.data)
    

    @action(methods=["POST"],url_name="register_websocket",detail=False,url_path="register-websocket")
    def register_websocket(self,request):
        """
            注册websocketID
        """
        # user_id = request.user
        websocket_id = str(uuid.uuid4())
        # conversation_id = request.query_params.get("conversation_id")
        payload = {
            "websocket_id":websocket_id,
            # "conversation_id":conversation_id,
            "user_id":int(1),
            "exp": (datetime.datetime.now() + datetime.timedelta(days=1)).timestamp()
        }
        ## 获取当前 host
        host = request.get_host()
        ## 加密成ACCESS_TOKEN
        token = generate_jwt_token(payload,secret_key=settings.JWT_KEY)
        url = f"wss://www.weridolin.cn/ws-endpoint/api/v1/gpt?token={token}"
        return HTTPResponse(
            data={"websocket_uri":url,"websocket_id":websocket_id}
        )

class GptMessagePagination(PageNumberPaginationWrapper):
    page_size = 1000
    page_size_query_param = 'page_size'
    max_page_size = 1000


class GptMessageFilterSet(django_filters.FilterSet):
    #  省份信息筛选字段
    # title 为 request get的字段

    conversation_id = django_filters.CharFilter(
        lookup_expr="iexact", field_name="conversation_id")

    class Meta:
        model = GptMessage
        fields = ["conversation_id"]

from rest_framework.renderers import BaseRenderer

class ServerSentEventRenderer(BaseRenderer):
    media_type = "text/event-stream"
    format = "txt"

    def render(self, data, accepted_media_type=None, renderer_context=None):
        return data


class GptMessageViewSet(ModelViewSet):
    queryset=GptMessage.objects.all()
    serializer_class = GptMessageSerializer
    authentication_classes = [V1Authentication]
    permission_classes = []
    pagination_class = GptMessagePagination
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_class = GptMessageFilterSet

    def get_authenticators(self):
        if self.request.path == "/gpt/api/v1/message/update-result":
            return []
        return super().get_authenticators()

    def get_renderers(self):
        if self.request.path == "/gpt/api/v1/message/sse":
            return [ServerSentEventRenderer()]
        return super().get_renderers()

    def create(self, request, *args, **kwargs):
        user_id = int(request.user)
        ## 获取当前请求的完全路径
        # 查询对话上下文
        conversation_id = request.data.get("conversation_id")
        conversation = GptConversation.objects.filter(uuid=conversation_id).first()
        api_key = conversation.key
        history = list()
        history_messages = GptMessage.objects.filter(conversation_id=conversation_id).all().order_by("created")
        for message in history_messages:
            history.extend([{
                "role":"user",
                "content":message.query_content
            },{
                "role":"assistant",
                "content":message.reply_content or "no reply"
            }])
        history.append({
            "role":"user",
            "content":request.data.get("query_content")
        })
        ## 新的查询记录入库 
        request.data.update({
            "user_id":user_id,
            "api_key":api_key
        })
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        request.data.update({
            "history":history,
            "from_app":"gpt",
            "exp": (datetime.datetime.now() + datetime.timedelta(days=1)).timestamp()
        })
        request.data.update({
                "callback_url":f"svc-site-oldbackend:8000/gpt/api/v1/message/update-result",
                "callback_url_grpc":f"svc-site-oldbackend:50001"
            }
        )   

        ## 推送消息到websocket服务
        res = public_message(
            "rest-svc",
            "gpt.chat.message.query",
            json.dumps(request.data,ensure_ascii=False)
        )
        if res:
            return HTTPResponse(data=serializer.data,status=status.HTTP_201_CREATED)
        else:
            return HTTPResponse(
                message="推送消息失败!",
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

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
    
    @action(methods=["POST"],url_name="updateResult",detail=False,url_path="update-result")
    def updateResult(self,request):
        """
            采用websocket的情况下 GPT询问结果http回调,
        """
        user_id = int(request.user) 
        reply_content = request.data.get("content")
        query_message_id = request.data.get("query_message_id")
        interrupt = request.data.get("interrupt")
        interrupt_reason =request.data.get("interrupt_reason")
        error = request.data.get("error")
        error_code = request.data.get("error_code")
        error_detail = request.data.get("error_detail")
        res = GptMessage.objects.filter(uuid=query_message_id).update(
            reply_content=reply_content,
            interrupt=interrupt,
            interrupt_reason=interrupt_reason,
            error=error,
            error_code=error_code,
            error_detail=error_detail,
            reply_finish=True,
            has_sended=True,
            user_id=user_id
        )
        if not res:
            return HTTPResponse(
                data={"success":False},
                message="更新失败!"
            )
        return HTTPResponse(
            data={"success":True},
            message="更新成功!"
        )

    @action(methods=["POST"],url_name="stop-sse",detail=False,url_path="stop-sse")
    def stop_sse(self,request):
        """
            停止SSE回复
        """
        user_id = int(request.user)
        query_message_id = request.data.get("query_message_id")
        message =  GptMessage.objects.filter(uuid=query_message_id).first()
        if not message:
            return HTTPResponse(
                message="停止失败!未找到对应的请求",
                status=status.HTTP_404_NOT_FOUND
            )
        if message.user_id != user_id:
            return HTTPResponse(
                message="停止失败!无权限",
                status=status.HTTP_403_FORBIDDEN
            )
        req = get_manager().get_req(query_message_id)
        if req:
            req.stop()
            return HTTPResponse(
                message="停止成功!"
            )
        return HTTPResponse(
            message="停止失败!未找到对应的请求,或者请求已经结束",
            status=status.HTTP_404_NOT_FOUND
        )


#### sever send event
from channels.generic.http import AsyncHttpConsumer
import logging


class GptSSEConsumer(AsyncHttpConsumer):
    _req_manager = get_manager()    


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.keepalive = False
        self.has_start = False 
        self.req:HttpMixins = None

    async def handle(self, body):
        data = json.loads(body)
        user_id = int(self.scope['user_id'])
        id = data.get('uuid',str(uuid.uuid4()))
        # 查询对话上下文
        conversation_id = data.get("conversation_id")
        conversation = GptConversation.objects.filter(uuid=conversation_id).first()
        if not conversation:
            await self.send_error("conversation not found",404)
            return
        api_key = conversation.key
        history = list()
        history_messages = GptMessage.objects.filter(conversation_id=conversation_id).all().order_by("created")
        for message in history_messages:
            history.extend([{
                "role":"user",
                "content":message.query_content or "no reply"
            },{
                "role":"assistant",
                "content":message.reply_content or "no reply"
            }])
        history.append({
            "role":"user",
            "content":data.get("query_content")
        })
        data.update({
            "user_id":user_id,
            "uuid":id,
        })
        ## 新查的记录入库
        serializer = GptMessageSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        self.req = AliHttpRequest(message_id=id,async_consumer=self)
        self._req_manager.register_req(id,self)
        try:
            await self.req.request(
                model=data.get("model"),
                messages=history,
                stream=True,
                enable_search=False,
                incremental_output=True,
                conversation_id=conversation_id,
                api_key=api_key
            )
        except Exception as e:
            logger.error("get ali gpt reply error ",exc_info=True)
            await self.send_error(str(e))
            return
        finally:
            await self.disconnect(id=id)

        self.update_result(self.req,user_id=user_id)

    async def http_request(self, message):
        if "body" in message:
            self.body.append(message["body"])
        if not message.get("more_body"):
            await self.handle(b"".join(self.body))

    def update_result(self,req:HttpMixins,user_id=None):
        res = GptMessage.objects.filter(uuid=req.message_id).update(
            reply_content=req.total_reply,
            interrupt=req.interrupt,
            interrupt_reason=req.interrupt_reason,
            error=req.error,
            error_code=req.error_code,
            error_detail=req.error_detail,
            reply_finish=True,
            has_sended=True,
            user_id=user_id
        )
        if not res:
            logger.info("update result to db failed!")
        else:
            logger.info("update result to db success!")

    async def disconnect(self,id=None):
        self._req_manager.remove_req(id)
        return await super().disconnect()

    async def send_error(self,error_msg,error_code=500):
        # print("send error -> ",error_msg," error_code -> ",error_code)
        try:
            await self.send({
                "type": "http.response.start",
                "status": error_code,
                "headers": [
                    (b"content-type", b"text/plain"),
                ],
            })
        except ValueError as e:
            if "HTTP response has already been started" in str(e):
                pass
            else:
                raise
        body = b"event:error\nda"
        await self.send_body(error_msg.encode("utf-8"),more_body=False)

    def stop(self):
        self.req.error = False
        self.req.interrupt = True
        self.req.interrupt_reason = "manual stop"

### GRPC
from . import gpt_pb2_grpc
from . import gpt_pb2

class GptMessageRpcImpl(gpt_pb2_grpc.GptMessageServicer):
    """
        GPT rpc消息服务
    """

    async def UpdateQueryResult(self,request,context):
        """
            更新查询结果
        """
        ## 查询对话上下文
        # await  asyncio.sleep(0)
        try:
            reply_content = request.reply_content
            query_message_id = request.query_message_id
            interrupt = request.interrupt
            interrupt_reason =request.interrupt_reason
            error = request.error
            error_code = request.error_code
            error_detail = request.error_detail
            res = GptMessage.objects.filter(uuid=query_message_id).update(
                reply_content=reply_content,
                interrupt=interrupt,
                interrupt_reason=interrupt_reason,
                error=error,
                error_code=error_code,
                error_detail=error_detail,
                reply_finish=True,
                has_sended=True,
            )
            if res:
                response = gpt_pb2.UpdateQueryResultReply()
                response.success=True
            else:
                response = gpt_pb2.UpdateQueryResultReply()
                response.success=False
            return response
        except Exception as e:
            logger.error(f"grpc update query result error {e}",exc_info=True)
            response.success=False
            return response
