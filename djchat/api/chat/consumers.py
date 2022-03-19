import json

from channels.generic.websocket import AsyncWebsocketConsumer

from .logics import (
    get_room_or_error, new_message, message_to_user, 
    get_serialized_message, get_chat_group_name,
    get_user_group_name
)


class ChatConsumer(AsyncWebsocketConsumer):
    # Метод подключения к WS
    async def connect(self):
        print("ChatConsumer: connect: " + str(self.scope["user"]))

        room_id = self.scope['url_route']['kwargs']['id']
        self.room = await get_room_or_error(room_id)
        self.room_group_name = await get_chat_group_name(self.room)

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    # Метод для отключения пользователя
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Принимаем сообщение от пользователя
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message_text = text_data_json['message']
        message = await new_message(
            message=message_text, user=self.scope["user"], room=self.room
        )
        message_data = await get_serialized_message(message)

        # Отправляем сообщение 
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message_data,
            }
        )

        # Отправка сообщения в канал чатов
        await message_to_user(message)

    # Метод для отправки сообщения клиентам
    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'message': event['message']
        }))


class ChatsConsumer(AsyncWebsocketConsumer):
    # Метод подключения к WS
    async def connect(self):
        print("ChatsConsumer: connect: " + str(self.scope["user"]))

        self.room = await get_user_group_name(self.scope["user"])
        self.room_group_name = self.room

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    # Метод для отключения пользователя
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
 
    # Метод для отправки нового сообщения в список чатов
    async def new_message(self, event):
        await self.send(text_data=json.dumps({
            'message': event['message'],
        }, ensure_ascii=False))

