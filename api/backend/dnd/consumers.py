import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import User
from django.utils import timezone
from asgiref.sync import sync_to_async
from .models import Message

date_time_format = "%d.%m.%Y %H:%M:%S %Z"

class DMConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("game", self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        target = data.get("target", "all")
        message_content = data.get("message", "")
        timezone.activate(timezone.get_default_timezone())
        timestamp = timezone.localtime(timezone.now()).strftime(date_time_format)

        if target == "all":
            await self.save_message(message_content, is_global=True)

            await self.channel_layer.group_send(
                "game",
                {
                    "type": "broadcast_message",
                    "target": "all",
                    "message": message_content,
                    "timestamp": timestamp,
                }
            )
        else:
            await self.save_message(message_content, is_global=False, target_username=target)

            await self.channel_layer.group_send(
                f"user_{target}",
                {
                    "type": "broadcast_message",
                    "target": target,
                    "message": message_content,
                    "timestamp": timestamp,
                }
            )

        timezone.deactivate()
    
    async def save_message(self, content, is_global, target_username=None):
        target_user = None
        if target_username and not is_global:
            try:
                target_user = await sync_to_async(User.objects.get)(username=target_username)
            except User.DoesNotExist:
                pass
        
        await sync_to_async(Message.objects.create)(
            content=content,
            is_global=is_global,
            target_player=target_user
        )


class PlayerConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        self.user_group_name = f"user_{self.scope['user'].username}"
        await self.channel_layer.group_add("game", self.channel_name)
        await self.channel_layer.group_add(self.user_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("game", self.channel_name)
        await self.channel_layer.group_discard(self.user_group_name, self.channel_name)

    async def force_artwork(self, event):
        title = event["title"]
        filename = event["filename"]
        await self.send(text_data=json.dumps({
            "type": "force_artwork",
            "title": title,
            "filename": filename
        }))
    
    async def remove_force_artwork(self, event):
        await self.send(text_data=json.dumps({
            "type": "remove_force_artwork",
        }))

    async def remove_artwork(self, event):
        artwork_id = event["artwork_id"]
        await self.send(text_data=json.dumps({
            "type": "remove_artwork",
            "artwork_id": artwork_id,
        }))

    async def broadcast_message(self, event):
        target = event["target"]
        message = event["message"]
        timestamp = event["timestamp"]

        if target == "all" or target == self.scope['user'].username:
            await self.send(text_data=json.dumps({
                "message": message,
                "timestamp": timestamp,
            }))
