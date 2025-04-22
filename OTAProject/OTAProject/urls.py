# OTAProject/OTAProject/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from OTA import views as ota_views

urlpatterns = [
    path('admin/', admin.site.urls),

    # 认证相关
    path('', ota_views.index, name='index'),
    path('login/', ota_views.login_view, name='login'),
    path('register/', ota_views.register_view, name='register'),
    path('logout/', ota_views.logout_view, name='logout'),

    # API端点
    path('api/login/', ota_views.login_api, name='api_login'),
    path('api/register/', ota_views.register_api, name='api_register'),
    path('api/travel-agencies/', ota_views.travel_agencies_api, name='api_travel_agencies'),

    # 仪表板
    path('agency/dashboard/', ota_views.agency_dashboard, name='agency_dashboard'),
    path('guide/dashboard/', ota_views.guide_dashboard, name='guide_dashboard'),
    path('tourist/dashboard/', ota_views.tourist_dashboard, name='tourist_dashboard'),
    path('admin/dashboard/', ota_views.admin_dashboard, name='admin_dashboard'),

    # 路线管理
    path('api/routes/', ota_views.routes_api, name='api_routes'),
    path('api/routes/<int:route_id>/', ota_views.route_detail_api, name='api_route_detail'),

    # 导游相关
    path('api/guides/', ota_views.guides_api, name='api_guides'),

    # 游客管理
    path('api/tourists/', ota_views.tourists_api, name='api_tourists'),
    path('api/bookings/<int:booking_id>/confirm/', ota_views.confirm_booking_api, name='api_confirm_booking'),
    path('api/bookings/<int:booking_id>/cancel/', ota_views.cancel_booking_api, name='api_cancel_booking'),

    # 行程管理
    path('api/itineraries/', ota_views.itineraries_api, name='api_itineraries'),
    path('api/itineraries/<int:itinerary_id>/cancel/', ota_views.cancel_itinerary_api, name='api_cancel_itinerary'),

    # 投诉管理
    path('api/complaints/', ota_views.complaints_api, name='api_complaints'),

    # 聊天相关
    path('chat/', include('chat.urls')),
]

# 开发环境中提供媒体文件服务
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)