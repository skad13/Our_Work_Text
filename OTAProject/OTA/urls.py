# OTAProject/OTAApp/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),

    path('agency/dashboard/', views.agency_dashboard, name='agency_dashboard'),
    path('guide/dashboard/', views.guide_dashboard, name='guide_dashboard'),
    path('tourist/dashboard/', views.tourist_dashboard, name='tourist_dashboard'),
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),

    # API端点
    path('api/login/', views.login_api, name='login_api'),
    path('api/register/', views.register_api, name='register_api'),
    path('api/travel-agencies/', views.travel_agencies_api, name='travel_agencies_api'),
    path('api/routes/', views.routes_api, name='routes_api'),
    path('api/routes/<int:route_id>/', views.route_detail_api, name='route_detail_api'),
    path('api/guides/', views.guides_api, name='guides_api'),
    path('api/tourists/', views.tourists_api, name='tourists_api'),
    path('api/bookings/<int:booking_id>/confirm/', views.confirm_booking_api, name='confirm_booking_api'),
    path('api/bookings/<int:booking_id>/cancel/', views.cancel_booking_api, name='cancel_booking_api'),
    path('api/itineraries/', views.itineraries_api, name='itineraries_api'),
    path('api/itineraries/<int:itinerary_id>/cancel/', views.cancel_itinerary_api, name='cancel_itinerary_api'),
]