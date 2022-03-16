from rest_framework.generics import RetrieveAPIView, ListAPIView
from rest_framework import permissions
from rest_framework.pagination import LimitOffsetPagination

from django.shortcuts import render
from django.shortcuts import get_object_or_404

from .models import Message, Room
from .serializers import RoomsSerializer, MessageSerializer, RoomSerializer

def index(request):
    rooms = Room.objects.all()

    return render(request, 'chat/index.html', {
        'rooms' : rooms
    })

def room(request, room_name):
    room_obj = get_object_or_404(Room, name=room_name)

    messages = Message.objects.filter(room=room_obj)

    return render(request, 'chat/room.html', {
        'room_name': room_name,
        'messages' : messages
    })


class ChatListApiView(ListAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomsSerializer
    permission_classes = [permissions.IsAuthenticated]


class ChatRetrieveAPIView(RetrieveAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = "name"
  

class ChatMessagesListAPIView(ListAPIView):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        room_name = self.kwargs['name']
        room_obj = get_object_or_404(Room, name=room_name)
        return room_obj.message_room.all()