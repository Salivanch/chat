from django.urls import path

from . import views

urlpatterns = [
    # path('', views.index, name='index'),
    # path('<str:room_name>/', views.room, name='room'),

    path('', views.ChatListApiView.as_view()),
    path('<str:name>/', views.ChatRetrieveAPIView.as_view()),
    path('<str:name>/messages', views.ChatMessagesListAPIView.as_view()),
]