from django.db.models import Manager, Max, Q


class PrivateChatRoomManager(Manager):
    def get_queryset(self):
        return super().get_queryset().alias(
            latest_message=Max('message_room__timestamp')
        ).order_by('-latest_message')

    def by_user(self, user):
        return self.get_queryset().filter(
            Q(user1=user) | Q(user2=user)
        )

    def by_users(self, user1, user2):
        return self.get_queryset().filter(
            (Q(user1=user1) | Q(user2=user1)) & (Q(user1=user2) | Q(user2=user2))
        )


class RoomChatMessageManager(Manager):
    def get_queryset(self):
        return super().get_queryset().order_by("-timestamp")

    def by_room_id(self, room_id):
        return self.get_queryset().select_related('room').filter(room__id=room_id)