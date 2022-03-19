from rest_framework.generics import RetrieveAPIView, ListAPIView, GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response

from .models import PrivateChatRoom, RoomChatMessage
from .serializers import RoomsSerializer, RoomSerializer, SimpleMessageSerializer
from .permission import (
    IsChatUserAndIsAuthenticatedRetrive, IsChatUserAndIsAuthenticatedList
)
from .logics import get_or_create_chat, get_user_or_error


class ChatListApiView(ListAPIView):
    serializer_class = RoomsSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return PrivateChatRoom.objects.by_user(self.request.user)

    def get_serializer_context(self):
        return {'user': self.request.user}


class ChatRetrieveAPIView(RetrieveAPIView):
    queryset = PrivateChatRoom.objects.all()
    serializer_class = RoomSerializer
    permission_classes = [IsChatUserAndIsAuthenticatedRetrive]


class ChatMessagesListAPIView(ListAPIView):
    serializer_class = SimpleMessageSerializer
    permission_classes = [IsChatUserAndIsAuthenticatedList]
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        return RoomChatMessage.objects.by_room_id(self.kwargs['pk'])


class GetOrCreateChatApi(GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        find_user = get_user_or_error(kwargs['id'])
        room_id = get_or_create_chat(find_user, self.request.user)
        return Response({"room_id": room_id})