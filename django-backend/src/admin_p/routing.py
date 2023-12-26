from django.urls import re_path

from admin_p import cunsomer

websocket_urlpatterns = [
    re_path(r'ws/notification/', cunsomer.Notification.as_asgi())
]