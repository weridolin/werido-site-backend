
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from ws.const import WSMessageType

class DataFakerConsumer(AsyncWebsocketConsumer):
    """
        datafaker-ws:
            {
                "type":WSMessageType,
                "data":"",
                "key":""
            }    
    """
    async def connect(self):
        # print(">>>>>>>>>>>",self.scope,type(self.scope))
        self.key = self.scope['url_route']['kwargs']['key']
        self.key_group_name = 'dataFaker_%s' % self.key ## socket连接的唯一标识？
        # Join room group
        await self.channel_layer.group_add(
            self.key_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.key_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        try:
            text_data_json = json.loads(text_data)
        except json.JSONDecodeError:
            message = f"get invalid json format data:{text_data}"
        except Exception as exc:
            message = f"an error raise:{exc}"
        if text_data_json.get("type",None)== WSMessageType.start:
            ## START CREATE TASK
            ...
        elif text_data_json.get("type",None)== WSMessageType.stop:
            ...

        # Send message to room group,
        await self.channel_layer.group_send(
            self.key_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))