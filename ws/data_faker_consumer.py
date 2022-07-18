import json,asyncio
from channels.generic.websocket import AsyncWebsocketConsumer
from ws.const import WSMessageType
from dataFaker.dfaker import create_task_async

## 所有的 WS连接都是一个线程里面的 receive
class DataFakerConsumer(AsyncWebsocketConsumer):
    """
        datafaker-ws:
            {
                "type":WSMessageType,
                "data":{
                    "dataCount":
                },
                "record_key":""
            }    
    """
    async def connect(self):
        self.key = self.scope['url_route']['kwargs']['key']
        self.key_group_name = 'dataFaker_%s' % self.key ## socket连接的唯一标识？
        # Join room group
        await self.channel_layer.group_add(
            self.key_group_name,
            self.channel_name
        )
        await self.accept()
        await self.send(text_data=json.dumps({
                "type":WSMessageType.start,
                "data":{},
                "record_key":self.key
            })
        )

    async def disconnect(self, close_code):
        print(f">>> close websocket 链接({self.key})")
        await self.channel_layer.group_discard(
            self.key_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        try:
            text_data_json = json.loads(text_data)
            print("receive ws message",text_data_json)
            if text_data_json.get("type",None)== WSMessageType.start:
                ## START CREATE TASK
                record_key = text_data_json.get("record_key",None)
                asyncio.run_coroutine_threadsafe(
                    create_task_async(
                        record_key=record_key,
                        ws=self), 
                    asyncio.get_running_loop()
                ).add_done_callback(_on_done_callback)
            elif text_data_json.get("type",None)== WSMessageType.stop:
                ...# TODO
            message = "generating data ing..."
        except json.JSONDecodeError:
            message = f"get invalid json format data:{text_data}"
        except Exception as exc:
            message = f"an error raise:{exc}"

    async def chat_message(self, event):
        message = event['message']
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        })) 


def _on_done_callback(future):
    target_path,ws = future.result()
    print(">>>>>>>>>> on done callback","target_path:",target_path,ws)
    