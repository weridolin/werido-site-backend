from channels.generic.websocket import AsyncWebsocketConsumer
import json,asyncio
from ws.const import ChatGPTMessageType
from thirdApis.chatGPT.chat_async_tasks import chatGPT_create_request,chatGPT_callback
class ChatGPTMessageConsumer(AsyncWebsocketConsumer):
    """
        chatGPT-ws:
            {
                "type":WSMessageType,
                "data":{
                    "query_content":"",
                    "parent_message_id":"",
                    "reply_content":"",
                    "uuid":"",
                    "id":"", 
                    "conversation_id":"",
                }
            }    
    """
    async def connect(self):
        self.user_id = self.scope['url_route']['kwargs']['user_id']
        self.key_group_name = 'chatGPT_%s' % self.user_id ## socket连接的唯一标识？
        # Join room group
        await self.channel_layer.group_add(
            self.key_group_name,
            self.channel_name
        )
        await self.accept()
        await self.send(text_data=json.dumps({
                "type":ChatGPTMessageType.connect,
                "data":{},
                "user_id":self.user_id
            })
        )

    async def disconnect(self, close_code):
        print(f"ch close websocket 链接({self.user_id})")
        await self.channel_layer.group_discard(
            self.key_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        try:
            text_data_json = json.loads(text_data)
            print("receive ws message",text_data_json)
            if text_data_json.get("type",None)== ChatGPTMessageType.query:
                ## START CREATE TASK
                data = text_data_json.get("data",None)
                asyncio.run_coroutine_threadsafe(
                    chatGPT_create_request(
                        data=data,
                        ws=self), 
                    asyncio.get_running_loop()
                ).add_done_callback(chatGPT_callback)
            elif text_data_json.get("type",None)== ChatGPTMessageType.disconnect:
                ...# TODO
            message = "generating data ing..."
        except json.JSONDecodeError:
            message = f"get invalid json format data:{text_data}"
        except Exception as exc:
            message = f"an error raise:{exc}"

