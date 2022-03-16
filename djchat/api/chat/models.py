from django.db import models
from django.conf import settings


class Room(models.Model):
    name = models.CharField(max_length=255, unique=True)


class Message(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, default=None, null=True, related_name="message_room")
    text = models.CharField(max_length=255)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=None, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)