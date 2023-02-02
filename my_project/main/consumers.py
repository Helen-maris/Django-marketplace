import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async

from main.models import Ad


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        self.roomGroupName = f'group_{self.user.id}'
        await self.channel_layer.group_add(
            self.roomGroupName,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.roomGroupName,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        await self.channel_layer.group_send(
            self.roomGroupName, {
                "type": "sendMessage",
                "message": message,
            })

    async def sendMessage(self, event):
        message = event["message"]
        result = await self.get_name(message)
        await self.send(text_data=json.dumps({"message": message, "result": result}))

    @database_sync_to_async
    def get_name(self, search_word):
        search_res = Ad.objects.filter(name=search_word).values('pk')
        if search_res:
            ad_pk = search_res[0]['pk']
            return f'http://127.0.0.1:8000/ads/{ad_pk}/'
        else:
            return None
