import json

from channels.generic.websocket import AsyncWebsocketConsumer


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = "global_chat"
        self.room_group_name = f"chat_{self.room_name}"

        # Присоединяемся к группе
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Покидаем группу при отключении
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        username = "Anonymous"  # Пока без авторизации

        # Отправляем сообщение ВСЕМ в группе
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': username
            }
        )

    # Получаем сообщения из группы
    async def chat_message(self, event):
        message = event['message']
        username = event['username']

        # Отправляем сообщение обратно WebSocket клиенту
        await self.send(text_data=json.dumps({
            'message': f"{username}: {message}",
            'type': 'chat'
        }))
