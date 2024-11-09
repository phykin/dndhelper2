import json
from channels.generic.websocket import AsyncWebsocketConsumer

class DMConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("game", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("game", self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        await self.channel_layer.group_send(
            "game",
            {
                "type": "broadcast_message",
                "message": data["message"],
            }
        )

    async def broadcast_message(self, event):
        await self.send(text_data=json.dumps({
            "message": event["message"]
        }))


class PlayerConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("game", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("game", self.channel_name)

    async def broadcast_message(self, event):
        await self.send(text_data=json.dumps({
            "message": event["message"]
        }))
