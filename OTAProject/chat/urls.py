from django.urls import path
from . import views

urlpatterns = [
    path('rooms/', views.get_chat_rooms, name='chat_rooms'),
    path('rooms/<int:room_id>/messages/', views.get_chat_messages, name='chat_messages'),
    path('rooms/<int:room_id>/send/', views.send_message, name='send_message'),
    path('rooms/create/', views.create_chat_room, name='create_chat_room'),
    path('notifications/', views.get_notifications, name='get_notifications'),
    path('notifications/<int:notification_id>/read/', views.mark_notification_as_read, name='mark_notification_as_read'),
    path('notifications/read-all/', views.mark_all_notifications_as_read, name='mark_all_notifications_as_read'),
]