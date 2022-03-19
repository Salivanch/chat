from django.db import models
from django.conf import settings

from .managers import PrivateChatRoomManager, RoomChatMessageManager


class PrivateChatRoom(models.Model):
    user1 = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="room_user1")
    user2 = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="room_user2")

    objects = PrivateChatRoomManager()


class RoomChatMessage(models.Model):
    room = models.ForeignKey(PrivateChatRoom, on_delete=models.CASCADE, related_name="message_room")
    text = models.TextField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=None, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = RoomChatMessageManager()
