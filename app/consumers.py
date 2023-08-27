from channels.generic.websocket import AsyncWebsocketConsumer
import json

class VideoConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = "app_%s" % self.room_name

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        video_id = text_data_json.get('video_id')  # Use get() to avoid KeyError
        message = text_data_json.get('message')  # Use get() to avoid KeyError
        state = text_data_json.get('state')
        currentTime = text_data_json.get('currentTime')
        
        if message is not None:
            await self.channel_layer.group_send(
                self.room_group_name,
                {"type": "chat_message", "message": message}
            )

        if video_id:
            await self.channel_layer.group_send(
                self.room_group_name,
                {"type": "send_video_id", "video_id": video_id}
            )
        if state:
            await self.channel_layer.group_send(
                self.room_group_name,
                {"type": "send_state", "state": state}
            )

    async def send_video_id(self, event):
        await self.send(text_data=json.dumps({
            'video_id': event['video_id']
        }))

    async def chat_message(self, event):
        message = event["message"]
        await self.send(text_data=json.dumps({"message": message}))

    async def send_state(self,event):
         await self.send(text_data=json.dumps({
            'state': event['state']
        }))

    async def send_currentTime(self,event):
         await self.send(text_data=json.dumps({
            'currentTime': event['currentTime']
        }))