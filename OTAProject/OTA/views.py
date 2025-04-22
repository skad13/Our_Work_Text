# OTAProject/OTAApp/views.py
import json
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import ensure_csrf_cookie
from .models import User, TravelAgency, Guide, Tourist, Route, RoutePoint, PointImage, Itinerary, Booking


def index(request):
    return render(request, 'index.html')


@ensure_csrf_cookie
def login_view(request):
    if request.user.is_authenticated:
        # 已登录用户根据类型重定向
        if request.user.user_type == 'travel_agency':
            return redirect('/agency/dashboard/')
        elif request.user.user_type == 'guide':
            return redirect('/guide/dashboard/')
        elif request.user.user_type == 'tourist':
            return redirect('/tourist/dashboard/')
        elif request.user.user_type == 'tourism_bureau':
            return redirect('/admin/dashboard/')

    return render(request, 'registration/login.html')


@ensure_csrf_cookie
def register_view(request):
    return render(request, 'registration/register.html')


def login_api(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            # 根据用户类型返回不同的重定向URL
            if user.user_type == 'travel_agency':
                redirect_url = '/agency/dashboard/'
            elif user.user_type == 'guide':
                redirect_url = '/guide/dashboard/'
            elif user.user_type == 'tourist':
                redirect_url = '/tourist/dashboard/'
            elif user.user_type == 'tourism_bureau':
                redirect_url = '/admin/dashboard/'
            else:
                redirect_url = '/'

            return JsonResponse({'success': True, 'redirect_url': redirect_url})
        else:
            return JsonResponse({'success': False, 'error': '用户名或密码不正确'})

    return JsonResponse({'success': False, 'error': '请求方法不支持'}, status=405)


def register_api(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            username = data.get('username')
            password = data.get('password')
            email = data.get('email')
            phone = data.get('phone')
            user_type = data.get('user_type')

            # 检查用户名是否已存在
            if User.objects.filter(username=username).exists():
                return JsonResponse({'success': False, 'error': '用户名已存在'})

            # 创建基本用户
            user = User.objects.create_user(
                username=username,
                password=password,
                email=email,
                phone=phone,
                user_type=user_type
            )

            # 根据用户类型创建相应记录
            if user_type == 'guide':
                guide_id = data.get('guide_id')
                travel_agency_id = data.get('travel_agency_id')

                # 验证导游特有字段
                if not guide_id or not travel_agency_id:
                    user.delete()
                    return JsonResponse({'success': False, 'error': '导游信息不完整'})

                try:
                    travel_agency = TravelAgency.objects.get(id=travel_agency_id)
                    Guide.objects.create(
                        user=user,
                        guide_id=guide_id,
                        travel_agency=travel_agency
                    )
                except TravelAgency.DoesNotExist:
                    user.delete()
                    return JsonResponse({'success': False, 'error': '所选旅行社不存在'})

            elif user_type == 'travel_agency':
                agency_name = data.get('agency_name')
                license_number = data.get('license_number')
                address = data.get('address', '')

                # 验证旅行社特有字段
                if not agency_name or not license_number:
                    user.delete()
                    return JsonResponse({'success': False, 'error': '旅行社信息不完整'})

                TravelAgency.objects.create(
                    user=user,
                    agency_name=agency_name,
                    license_number=license_number,
                    address=address
                )

            elif user_type == 'tourist':
                Tourist.objects.create(user=user)

            return JsonResponse({'success': True})

        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

    return JsonResponse({'success': False, 'error': '请求方法不支持'}, status=405)


def logout_view(request):
    logout(request)
    return redirect('/login/')


@login_required
def agency_dashboard(request):
    if request.user.user_type != 'travel_agency':
        return redirect('/login/')

    return render(request, 'dashboard/agency.html')


@login_required
def guide_dashboard(request):
    if request.user.user_type != 'guide':
        return redirect('/login/')

    return render(request, 'dashboard/guide.html')


@login_required
def tourist_dashboard(request):
    if request.user.user_type != 'tourist':
        return redirect('/login/')

    return render(request, 'dashboard/tourist.html')


@login_required
def admin_dashboard(request):
    if request.user.user_type != 'tourism_bureau':
        return redirect('/login/')

    return render(request, 'dashboard/admin.html')


# API端点 - 获取旅行社列表
def travel_agencies_api(request):
    agencies = TravelAgency.objects.all()
    data = {
        'travel_agencies': [
            {
                'id': agency.id,
                'name': agency.agency_name
            }
            for agency in agencies
        ]
    }
    return JsonResponse(data)


# API端点 - 路线管理
@login_required
def routes_api(request):
    if request.method == 'GET':
        # 获取当前旅行社的所有路线
        if request.user.user_type == 'travel_agency':
            routes = Route.objects.filter(travel_agency=request.user.travel_agency)
        else:
            routes = Route.objects.filter(is_published=True)

        data = {
            'routes': [
                {
                    'id': route.id,
                    'name': route.name,
                    'description': route.description,
                    'point_count': route.points.count()
                }
                for route in routes
            ]
        }
        return JsonResponse(data)

    elif request.method == 'POST':
        # 只允许旅行社创建路线
        if request.user.user_type != 'travel_agency':
            return JsonResponse({'success': False, 'error': '权限不足'}, status=403)

        try:
            data = json.loads(request.body)

            # 创建新路线
            route = Route.objects.create(
                name=data['name'],
                description=data.get('description', ''),
                travel_agency=request.user.travel_agency
            )

            # 添加路线点
            for i, point_data in enumerate(data['points']):
                RoutePoint.objects.create(
                    route=route,
                    name=point_data['name'],
                    latitude=point_data['latitude'],
                    longitude=point_data['longitude'],
                    description=point_data.get('description', ''),
                    order=i
                )

            return JsonResponse({'success': True, 'route_id': route.id})

        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

    return JsonResponse({'success': False, 'error': '请求方法不支持'}, status=405)


# API端点 - 单个路线详情
@login_required
def route_detail_api(request, route_id):
    route = get_object_or_404(Route, id=route_id)

    # 检查权限
    if not route.is_published and request.user.user_type != 'travel_agency':
        return JsonResponse({'success': False, 'error': '权限不足'}, status=403)

    if request.method == 'GET':
        points = route.points.all().order_by('order')

        data = {
            'route': {
                'id': route.id,
                'name': route.name,
                'description': route.description,
            },
            'points': [
                {
                    'id': point.id,
                    'name': point.name,
                    'latitude': point.latitude,
                    'longitude': point.longitude,
                    'description': point.description,
                    'order': point.order
                }
                for point in points
            ]
        }
        return JsonResponse(data)

    elif request.method == 'DELETE':
        # 只允许创建该路线的旅行社删除
        if request.user.user_type != 'travel_agency' or route.travel_agency.user != request.user:
            return JsonResponse({'success': False, 'error': '权限不足'}, status=403)

        try:
            route.delete()
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

    return JsonResponse({'success': False, 'error': '请求方法不支持'}, status=405)


# API端点 - 获取导游列表
@login_required
def guides_api(request):
    if request.user.user_type != 'travel_agency':
        return JsonResponse({'success': False, 'error': '权限不足'}, status=403)

    guides = Guide.objects.filter(travel_agency=request.user.travel_agency)
    data = {
        'guides': [
            {
                'id': guide.id,
                'name': guide.user.username,
                'guide_id': guide.guide_id
            }
            for guide in guides
        ]
    }
    return JsonResponse(data)


# API端点 - 获取游客报名列表
@login_required
def tourists_api(request):
    if request.user.user_type != 'travel_agency':
        return JsonResponse({'success': False, 'error': '权限不足'}, status=403)

    # 获取该旅行社所有行程的所有预订
    bookings = Booking.objects.filter(
        itinerary__route__travel_agency=request.user.travel_agency
    ).select_related('tourist__user', 'itinerary__route')

    data = {
        'tourists': [
            {
                'booking_id': booking.id,
                'name': booking.tourist.user.username,
                'phone': booking.tourist.user.phone,
                'itinerary_name': f"{booking.itinerary.route.name} ({booking.itinerary.start_date})",
                'status': dict(Booking.STATUS_CHOICES).get(booking.status),
                'created_at': booking.created_at.isoformat()
            }
            for booking in bookings
        ]
    }
    return JsonResponse(data)


# API端点 - 确认游客预订
@login_required
def confirm_booking_api(request, booking_id):
    if request.user.user_type != 'travel_agency' or request.method != 'POST':
        return JsonResponse({'success': False, 'error': '权限不足或请求方法不支持'}, status=403)

    booking = get_object_or_404(Booking, id=booking_id)

    # 确保只有对应旅行社才能确认预订
    if booking.itinerary.route.travel_agency.user != request.user:
        return JsonResponse({'success': False, 'error': '权限不足'}, status=403)

    booking.status = 'confirmed'
    booking.save()

    return JsonResponse({'success': True})


# API端点 - 取消游客预订
@login_required
def cancel_booking_api(request, booking_id):
    if request.user.user_type != 'travel_agency' or request.method != 'POST':
        return JsonResponse({'success': False, 'error': '权限不足或请求方法不支持'}, status=403)

    booking = get_object_or_404(Booking, id=booking_id)

    # 确保只有对应旅行社才能取消预订
    if booking.itinerary.route.travel_agency.user != request.user:
        return JsonResponse({'success': False, 'error': '权限不足'}, status=403)

    booking.status = 'cancelled'
    booking.save()

    return JsonResponse({'success': True})


# API端点 - 获取行程列表
@login_required
def itineraries_api(request):
    if request.method == 'GET':
        if request.user.user_type == 'travel_agency':
            # 旅行社查看自己的行程
            itineraries = Itinerary.objects.filter(route__travel_agency=request.user.travel_agency)
        elif request.user.user_type == 'guide':
            # 导游查看自己被指派的行程
            itineraries = Itinerary.objects.filter(guide=request.user.guide)
        elif request.user.user_type == 'tourist':
            # 游客查看所有公开行程
            itineraries = Itinerary.objects.filter(status='active', route__is_published=True)
        else:
            # 文旅局查看所有行程
            itineraries = Itinerary.objects.all()

        data = {
            'itineraries': [
                {
                    'id': itinerary.id,
                    'route_name': itinerary.route.name,
                    'start_date': itinerary.start_date.isoformat(),
                    'end_date': itinerary.end_date.isoformat() if itinerary.end_date else None,
                    'guide_name': itinerary.guide.user.username if itinerary.guide else None,
                    'status': dict(Itinerary.STATUS_CHOICES).get(itinerary.status),
                    'tourist_count': itinerary.bookings.count(),
                    'max_tourists': itinerary.max_tourists
                }
                for itinerary in itineraries
            ]
        }
        return JsonResponse(data)

    elif request.method == 'POST':
        # 只允许旅行社创建行程
        if request.user.user_type != 'travel_agency':
            return JsonResponse({'success': False, 'error': '权限不足'}, status=403)

        try:
            data = json.loads(request.body)

            route_id = data.get('route_id')
            start_date = data.get('start_date')
            guide_id = data.get('guide_id')
            max_tourists = data.get('max_tourists', 20)

            # 验证路线是否属于该旅行社
            route = get_object_or_404(Route, id=route_id)
            if route.travel_agency.user != request.user:
                return JsonResponse({'success': False, 'error': '该路线不属于您的旅行社'}, status=403)

            # 如果提供了导游ID，验证导游是否属于该旅行社
            guide = None
            if guide_id:
                guide = get_object_or_404(Guide, id=guide_id)
                if guide.travel_agency.user != request.user:
                    return JsonResponse({'success': False, 'error': '该导游不属于您的旅行社'}, status=403)

            # 创建行程
            itinerary = Itinerary.objects.create(
                route=route,
                start_date=start_date,
                guide=guide,
                max_tourists=max_tourists
            )

            return JsonResponse({'success': True, 'itinerary_id': itinerary.id})

        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

    return JsonResponse({'success': False, 'error': '请求方法不支持'}, status=405)


# API端点 - 取消行程
@login_required
def cancel_itinerary_api(request, itinerary_id):
    if request.user.user_type != 'travel_agency' or request.method != 'POST':
        return JsonResponse({'success': False, 'error': '权限不足或请求方法不支持'}, status=403)

    itinerary = get_object_or_404(Itinerary, id=itinerary_id)

    # 确保只有对应旅行社才能取消行程
    if itinerary.route.travel_agency.user != request.user:
        return JsonResponse({'success': False, 'error': '权限不足'}, status=403)

    itinerary.status = 'cancelled'
    itinerary.save()

    # 同时取消所有相关的预订
    Booking.objects.filter(itinerary=itinerary).update(status='cancelled')

    return JsonResponse({'success': True})