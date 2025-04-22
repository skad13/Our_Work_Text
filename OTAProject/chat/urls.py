# OTAProject/chat/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('api/contacts/', views.chat_contacts, name='chat_contacts'),
    path('api/history/', views.chat_history, name='chat_history'),
]