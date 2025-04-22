# OTAProject/chat/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.utils import timezone
from .models import ChatRoom, ChatMessage
from OTAApp.models import TravelAgency


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]

        # 只允许已认证用户
        if not self.user.is_authenticated:
            await self.close()
            return

        # 获取用户类型和ID
        self.user_type = self.user.user_type
        self.user_id = self.user.id

        if self.user_type == 'travel_agency':
            # 加入旅行社-文旅局群组
            self.agency_bureau_group = 'agency_bureau_group'
            await self.channel_layer.group_add(
                self.agency_bureau_group,
                self.channel_name
            )

        await self.accept()

    async def disconnect(self, close_code):
        # 离开群组
        if hasattr(self, 'agency_bureau_group'):
            await self.channel_layer.group_discard(
                self.agency_bureau_group,
                self.channel_name
            )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message_type = data.get('type')

        if message_type == 'chat_message':
            chat_id = data.get('chat_id')
            message = data.get('message')

            # 处理消息发送
            if chat_id == 'agency-group' and self.user_type == 'travel_agency':
                # 获取旅行社名称
                agency_name = await self.get_agency_name()

                # 发送到旅行社-文旅局群组
                await self.save_message(self.agency_bureau_group, message)
                await self.channel_layer.group_send(
                    self.agency_bureau_group,
                    {
                        'type': 'chat_message',
                        'chat_id': chat_id,
                        'sender': agency_name,
                        'message': message,
                        'timestamp': timezone.now().isoformat()
                    }
                )

    async def chat_message(self, event):
        # 发送消息到WebSocket
        await self.send(text_data=json.dumps({
            'type': 'chat_message',
            'chat_id': event['chat_id'],
            'sender': event['sender'],
            'message': event['message'],
            'timestamp': event['timestamp']
        }))

    @database_sync_to_async
    def get_agency_name(self):
        if self.user_type == 'travel_agency':
            try:
                return self.user.travel_agency.agency_name
            except TravelAgency.DoesNotExist:
                return self.user.username
        return self.user.username

    @database_sync_to_async
    def save_message(self, room_id, message_content):
        # 获取或创建聊天室
        room, _ = ChatRoom.objects.get_or_create(room_id=room_id)

        # 创建消息
        ChatMessage.objects.create(
            room=room,
            sender=self.user,
            content=message_content
        )