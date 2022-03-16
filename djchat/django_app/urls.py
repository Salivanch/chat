from django.urls import path, include
from django.contrib import admin
from django.conf.urls.static import static
from django_app import settings

urlpatterns = [
    path('chats/', include('api.chat.urls')),
    path('admin/', admin.site.urls),

	#path to djoser end points
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)