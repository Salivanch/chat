from django.contrib import admin

from .models import RoomChatMessage, PrivateChatRoom


admin.site.register(RoomChatMessage)
admin.site.register(PrivateChatRoom)