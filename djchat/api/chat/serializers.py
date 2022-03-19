from rest_framework import serializers

from api.user.serializers import SimpleUserSerializer

from .models import PrivateChatRoom, RoomChatMessage
from .utils import relative_date, str_to_date


class SimpleRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrivateChatRoom
        fields = ("id",)


class RoomSerializer(serializers.ModelSerializer):
    user1 = SimpleUserSerializer()
    user2 = SimpleUserSerializer()

    class Meta:
        model = PrivateChatRoom
        fields = ("user1", "user2")


class RoomsSerializer(serializers.ModelSerializer):
    last_message = serializers.SerializerMethodField()
    to_user = serializers.SerializerMethodField()

    class Meta:
        model = PrivateChatRoom
        fields = ("id", "to_user", "last_message")

    def get_last_message(self, value):
        return SimpleMessageSerializer(value.message_room.last()).data

    def get_to_user(self, value):
        if self.context['user'] == value.user1:
            return SimpleUserSerializer(value.user2).data
        return SimpleUserSerializer(value.user1).data


class SimpleMessageSerializer(serializers.ModelSerializer):
    timestamp = serializers.SerializerMethodField()
    user = SimpleUserSerializer()

    class Meta:
        model = RoomChatMessage
        fields = ("id", "text", "user", "timestamp")

    def get_timestamp(self, value):
        date = str_to_date(value.timestamp)
        return relative_date(date, simple_format=True)


class MessageSerializer(serializers.ModelSerializer):
    room = SimpleRoomSerializer()
    timestamp = serializers.SerializerMethodField()
    user = SimpleUserSerializer()

    class Meta:
        model = RoomChatMessage
        fields = '__all__'

    def get_timestamp(self, value):
        date = str_to_date(value.timestamp)
        return relative_date(date)
