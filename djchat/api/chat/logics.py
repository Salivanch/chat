from channels.layers import get_channel_layer
from channels.db import database_sync_to_async

from django.shortcuts import get_object_or_404

from .models import Message, Room
from .serializers import MessageSerializer


# Функция для создания нового сообщения в БД
@database_sync_to_async
def new_message(message, user, room):
    return Message.objects.create(text=message, user=user, room=room)


# Функция для получения комнаты
@database_sync_to_async
def get_room_or_error(room_name):
    return get_object_or_404(Room, name=room_name)


# Функция для получения сериализированного сообщения
def get_serialized_message(message):
    serializer = MessageSerializer(message)
    return serializer.data


# Функция для отправки в канал частов последнего сообщения
async def message_to_user(room_group_name, message_data):
    channel_layer = get_channel_layer()
    user_room_name = "user"

    await channel_layer.group_send(
        user_room_name,
        {
            'type': 'new_message',
            'message_data': message_data,
            'room_group_name': room_group_name
        }
    )