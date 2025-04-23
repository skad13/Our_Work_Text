# OTAProject/chat/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('api/contacts/', views.chat_contacts_api, name='chat_contacts_api'),
    path('api/history/', views.chat_history_api, name='chat_history_api'),
]