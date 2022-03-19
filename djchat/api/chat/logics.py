from channels.layers import get_channel_layer
from channels.db import database_sync_to_async

from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

from .models import RoomChatMessage, PrivateChatRoom
from .serializers import MessageSerializer, SimpleMessageSerializer


User = get_user_model()


# Функция для получения названия канала чата
async def get_chat_group_name(room):
    return f"PrivateChatRoom-{room.id}"


# Функция для получения названия канала чатов пользователя
async def get_user_group_name(user):
    return f"ChatRoomsByUser-{user.id}"


# Функция для получения пользователя
def get_user_or_error(user_id):
    return get_object_or_404(User, id=user_id)


# Функция для получения или создания чата
def get_or_create_chat(user1, user2):
    result = PrivateChatRoom.objects.by_users(user1, user2)
    if not result:
        room = PrivateChatRoom.objects.create(user1=user1, user2=user2)
        room.save()
        return room.id
    return result.first().id


# Функция для проверки существует ли чат
def is_exists_chat(user, room_id):
    return PrivateChatRoom.objects.by_user(user).filter(id=room_id).exists()


# Функция для создания нового сообщения в БД
@database_sync_to_async
def new_message(message, user, room):
    return RoomChatMessage.objects.create(text=message, user=user, room=room)


# Функция для получения комнаты
@database_sync_to_async
def get_room_or_error(room_id):
    return get_object_or_404(PrivateChatRoom, id=room_id)


# Функция для получения сериализированного сообщения
async def get_serialized_message(message, simple=True):
    if simple:
        return SimpleMessageSerializer(message).data
    return MessageSerializer(message).data


# Функция для получения пользователей чата по сообщению
@database_sync_to_async
def get_chat_users(message):
    return [message.room.user1, message.room.user2]


# Функция для отправки в канал частов последнего сообщения
async def message_to_user(message):
    channel_layer = get_channel_layer()

    message_data = await get_serialized_message(message, simple=False)
    room_users = await get_chat_users(message)
    for user in room_users:
        user_room_name = await get_user_group_name(user)

        await channel_layer.group_send(
            user_room_name,
            {
                'type': 'new_message',
                'message': message_data,
            }
        )