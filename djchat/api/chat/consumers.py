import json

from channels.generic.websocket import AsyncWebsocketConsumer

from .logics import get_room_or_error, new_message, message_to_user, get_serialized_message


class ChatConsumer(AsyncWebsocketConsumer):
    # Метод подключения к WS
    async def connect(self):
        print("ChatConsumer: connect: " + str(self.scope["user"]))

        room = await get_room_or_error(self.scope['url_route']['kwargs']['room_name'])
        self.room_group_name = room.name

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
        message = text_data_json['message']

        room = await get_room_or_error(self.room_group_name)
        message = await new_message(message=message, user=self.scope["user"], room=room)

        message_data = get_serialized_message(message)

        # Отправляем сообщение 
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message_data,
            }
        )

        # Отправка сообщения в канал частов
        await message_to_user(self.room_group_name, message_data)

    # Метод для отправки сообщения клиентам
    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'message': event['message']
        }))


class ChatsConsumer(AsyncWebsocketConsumer):
    # Метод подключения к WS
    async def connect(self):
        print("ChatsConsumer: connect: " + str(self.scope["user"]))

        room = "user"
        self.room_group_name = room

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
            'message_data': event['message_data'],
            'room_name': event['room_group_name']
        }, ensure_ascii=False))

