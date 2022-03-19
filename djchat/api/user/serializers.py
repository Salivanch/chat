from rest_framework import serializers

from .models import User


class SimpleUserSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'username', 'photo')

    def get_username(self, value):
        return value.get_display_name()