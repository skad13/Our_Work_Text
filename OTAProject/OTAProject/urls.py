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
    # 个人设置相关
    path('api/profile/', ota_views.get_profile_api, name='api_get_profile'),
    path('api/profile/update/', ota_views.update_profile_api, name='api_update_profile'),
    path('api/profile/upload-image/', ota_views.upload_profile_image, name='api_upload_profile_image'),

    # 旅行社仪表盘数据
    path('api/agency/dashboard/stats/', ota_views.agency_dashboard_stats, name='api_agency_dashboard_stats'),
    path('api/agency/guides/detail/', ota_views.agency_guides_detail, name='api_agency_guides_detail'),
    path('api/agency/bookings/detail/', ota_views.agency_bookings_detail, name='api_agency_bookings_detail'),
    path('api/agency/revenue/detail/', ota_views.agency_revenue_detail, name='api_agency_revenue_detail'),
    path('api/agency/itineraries/', ota_views.agency_itineraries, name='api_agency_itineraries'),

    # 路线管理 API
    path('api/agency/routes/', ota_views.agency_routes, name='api_agency_routes'),
    path('api/agency/routes/<int:route_id>/', ota_views.agency_route_detail, name='api_agency_route_detail'),
    path('api/agency/routes/<int:route_id>/points/', ota_views.agency_route_points, name='api_agency_route_points'),
    path('api/agency/routes/<int:route_id>/points/<int:point_id>/', ota_views.agency_route_point_detail, name='api_agency_route_point_detail'),
    path('api/agency/routes/<int:route_id>/points/<int:point_id>/images/', ota_views.upload_point_image, name='api_upload_point_image'),
    path('api/agency/routes/<int:route_id>/points/<int:point_id>/images/<int:image_id>/', ota_views.delete_point_image, name='api_delete_point_image'),

    # 导游管理 API
    path('api/agency/guides/', ota_views.agency_guides, name='api_agency_guides'),
    path('api/agency/available-guides/', ota_views.available_guides, name='api_available_guides'),
    path('api/agency/guides/<int:guide_id>/recruit/', ota_views.recruit_guide, name='api_recruit_guide'),
    path('api/agency/guides/<int:guide_id>/fire/', ota_views.fire_guide, name='api_fire_guide'),
    path('api/agency/guides/<int:guide_id>/salary/', ota_views.update_guide_salary, name='api_update_guide_salary'),

    # 预订管理 API
    path('api/agency/normal-bookings/', ota_views.agency_normal_bookings, name='api_agency_normal_bookings'),
    path('api/agency/waitlist-bookings/', ota_views.agency_waitlist_bookings, name='api_agency_waitlist_bookings'),
    path('api/agency/bookings/<int:booking_id>/', ota_views.agency_booking_detail, name='api_agency_booking_detail'),
    path('api/agency/bookings/<int:booking_id>/confirm/', ota_views.agency_confirm_booking, name='api_agency_confirm_booking'),
    path('api/agency/bookings/<int:booking_id>/approve/', ota_views.agency_approve_booking, name='api_agency_approve_booking'),
    path('api/agency/bookings/<int:booking_id>/reject/', ota_views.agency_reject_booking, name='api_agency_reject_booking'),

    # 行程管理 API
    path('api/agency/manage-itineraries/', ota_views.agency_manage_itineraries, name='api_agency_manage_itineraries'),
    path('api/agency/manage-itineraries/<int:itinerary_id>/', ota_views.agency_itinerary_detail, name='api_agency_itinerary_detail'),
    path('api/agency/manage-itineraries/<int:itinerary_id>/cancel/', ota_views.agency_cancel_itinerary, name='api_agency_cancel_itinerary'),
    path('api/agency/available-routes/', ota_views.agency_available_routes, name='api_agency_available_routes'),
    path('api/agency/available-guides/', ota_views.agency_available_guides, name='api_agency_available_guides'),

    # 统计分析 API
    path('api/agency/statistics/revenue/', ota_views.agency_revenue_statistics, name='api_agency_revenue_statistics'),
    path('api/agency/statistics/popular-routes/', ota_views.agency_popular_routes, name='api_agency_popular_routes'),
    path('api/agency/statistics/tourist-sources/', ota_views.agency_tourist_sources, name='api_agency_tourist_sources'),
    path('api/agency/statistics/guide-performance/', ota_views.agency_guide_performance, name='api_agency_guide_performance'),
]

# 开发环境中提供媒体文件服务
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)