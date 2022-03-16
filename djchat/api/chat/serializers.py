from rest_framework import serializers

from .models import Room, Message
from .utils import relative_date, str_to_date


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'


class SimpleMessageSerializer(serializers.ModelSerializer):
    timestamp = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = ("text", "user", "timestamp")

    def get_timestamp(self, value):
        date = str_to_date(value.timestamp)
        return relative_date(date, simple_format=True)


class RoomsSerializer(serializers.ModelSerializer):
    last_message = serializers.SerializerMethodField()

    class Meta:
        model = Room
        fields = '__all__'

    def get_last_message(self, value):
        return SimpleMessageSerializer(value.message_room.last()).data


class MessageSerializer(serializers.ModelSerializer):
    # room = RoomSerializer()
    timestamp = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = '__all__'

    def get_timestamp(self, value):
        date = str_to_date(value.timestamp)
        return relative_date(date)
