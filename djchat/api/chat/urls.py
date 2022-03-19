from django.urls import path

from . import views

urlpatterns = [
    path('', views.ChatListApiView.as_view()),
    path('<int:pk>', views.ChatRetrieveAPIView.as_view()),
    path('<int:pk>/messages', views.ChatMessagesListAPIView.as_view()),
    path('by_user/<int:id>', views.GetOrCreateChatApi.as_view()),
]