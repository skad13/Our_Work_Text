# chat/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.utils import timezone
from .models import ChatMessage, ChatRoom


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]

        # 只允许已认证用户
        if not self.user.is_authenticated:
            await self.close()
            return

        # 获取旅行社ID
        if self.user.user_type == 'travel_agency':
            self.agency_id = self.user.travel_agency.id
        else:
            await self.close()
            return

        # 加入旅行社-文旅局群组
        self.agency_bureau_group = f'agency_bureau_group'
        await self.channel_layer.group_add(
            self.agency_bureau_group,
            self.channel_name
        )

        # 加入旅行社自己的频道，用于接收自己导游的消息
        self.agency_channel = f'agency_{self.agency_id}'
        await self.channel_layer.group_add(
            self.agency_channel,
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

        if hasattr(self, 'agency_channel'):
            await self.channel_layer.group_discard(
                self.agency_channel,
                self.channel_name
            )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message_type = data.get('type')

        if message_type == 'chat_message':
            chat_id = data.get('chat_id')
            message = data.get('message')

            # 处理消息发送
            if chat_id == 'agency-group':
                # 发送到文旅局-旅行社群组
                await self.save_message(self.agency_bureau_group, message)
                await self.channel_layer.group_send(
                    self.agency_bureau_group,
                    {
                        'type': 'chat_message',
                        'chat_id': chat_id,
                        'sender': f"{self.user.travel_agency.agency_name}",
                        'message': message,
                        'timestamp': timezone.now().isoformat()
                    }
                )
            elif chat_id.startswith('guide-'):
                # 发送给特定导游
                guide_id = chat_id.split('-')[1]
                guide_channel = f'guide_{guide_id}'
                await self.save_message(guide_channel, message)
                await self.channel_layer.group_send(
                    guide_channel,
                    {
                        'type': 'chat_message',
                        'chat_id': f'agency-{self.agency_id}',
                        'sender': f"{self.user.travel_agency.agency_name}",
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
    def save_message(self, room_id, message_content):
        # 获取或创建聊天室
        room, _ = ChatRoom.objects.get_or_create(room_id=room_id)

        # 创建消息
        ChatMessage.objects.create(
            room=room,
            sender=self.user,
            content=message_content
        )