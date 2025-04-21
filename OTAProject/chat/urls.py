# urls.py
from django.urls import path
from . import views
from .chat import views as chat_views

urlpatterns = [

    path('agency/dashboard/', views.agency_dashboard, name='agency_dashboard'),
    path('api/save-route/', views.save_route, name='save_route'),
    path('api/chat-contacts/', chat_views.chat_contacts, name='chat_contacts'),
    path('api/chat-history/', chat_views.chat_history, name='chat_history'),
    path('routes/', views.route_list, name='route_list'),
    path('logout/', views.logout_view, name='logout'),
]