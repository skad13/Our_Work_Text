# OTAProject/OTA/views.py
import json
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import ensure_csrf_cookie
from .models import User, TravelAgency, Guide, Tourist, Route, RoutePoint, PointImage, Itinerary, Booking, Complaint


def index(request):
    return redirect('login')


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

            elif user_type == 'tourism_bureau':
                # 文旅局用户不需要额外信息
                pass

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


# API端点 - 行程管理
@login_required
def itineraries_api(request):
    if request.method == 'GET':
        # 获取行程列表
        if request.user.user_type == 'travel_agency':
            itineraries = Itinerary.objects.filter(route__travel_agency=request.user.travel_agency)
        elif request.user.user_type == 'guide':
            itineraries = Itinerary.objects.filter(guide=request.user.guide)
        else:
            itineraries = Itinerary.objects.filter(status='active', is_published=True)

        itineraries = itineraries.select_related('route', 'guide__user')

        data = {
            'itineraries': [
                {
                    'id': itinerary.id,
                    'route_name': itinerary.route.name,
                    'start_date': itinerary.start_date.strftime('%Y-%m-%d'),
                    'guide_name': itinerary.guide.user.username if itinerary.guide else None,
                    'tourist_count': itinerary.bookings.count(),
                    'max_tourists': itinerary.max_tourists,
                    'status': dict(Itinerary.STATUS_CHOICES).get(itinerary.status)
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

            if not route_id or not start_date:
                return JsonResponse({'success': False, 'error': '行程信息不完整'})

            # 获取路线
            try:
                route = Route.objects.get(id=route_id, travel_agency=request.user.travel_agency)
            except Route.DoesNotExist:
                return JsonResponse({'success': False, 'error': '路线不存在或无权访问'})

            # 获取导游（如果提供）
            guide = None
            if guide_id:
                try:
                    guide = Guide.objects.get(id=guide_id, travel_agency=request.user.travel_agency)
                except Guide.DoesNotExist:
                    return JsonResponse({'success': False, 'error': '导游不存在或无权指派'})

            # 创建行程
            itinerary = Itinerary.objects.create(
                route=route,
                start_date=start_date,
                guide=guide,
                max_tourists=max_tourists
            )

            return JsonResponse({
                'success': True,
                'itinerary_id': itinerary.id
            })

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

    # 同时取消所有相关预订
    Booking.objects.filter(itinerary=itinerary).update(status='cancelled')

    return JsonResponse({'success': True})


# API端点 - 投诉管理
@login_required
def complaints_api(request):
    if request.method == 'POST':
        # 只允许游客提交投诉
        if request.user.user_type != 'tourist':
            return JsonResponse({'success': False, 'error': '权限不足'}, status=403)

        try:
            data = json.loads(request.body)

            title = data.get('title')
            content = data.get('content')
            itinerary_id = data.get('itinerary_id')

            if not title or not content:
                return JsonResponse({'success': False, 'error': '投诉信息不完整'})

            # 创建投诉
            complaint = Complaint(
                tourist=request.user.tourist,
                title=title,
                content=content
            )

            # 关联行程（如果提供）
            if itinerary_id:
                try:
                    itinerary = Itinerary.objects.get(id=itinerary_id)
                    complaint.itinerary = itinerary
                except Itinerary.DoesNotExist:
                    pass

            complaint.save()

            return JsonResponse({'success': True, 'complaint_id': complaint.id})

        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

    elif request.method == 'GET':
        # 文旅局可以查看所有投诉
        if request.user.user_type == 'tourism_bureau':
            complaints = Complaint.objects.all()
        # 旅行社只能查看自己行程的投诉
        elif request.user.user_type == 'travel_agency':
            complaints = Complaint.objects.filter(
                itinerary__route__travel_agency=request.user.travel_agency
            )
        # 导游只能查看自己带队的行程的投诉
        elif request.user.user_type == 'guide':
            complaints = Complaint.objects.filter(
                itinerary__guide=request.user.guide
            )
        # 游客只能查看自己的投诉
        elif request.user.user_type == 'tourist':
            complaints = Complaint.objects.filter(
                tourist=request.user.tourist
            )
        else:
            return JsonResponse({'success': False, 'error': '权限不足'}, status=403)

        complaints = complaints.select_related('tourist__user', 'itinerary__route')

        data = {
            'complaints': [
                {
                    'id': complaint.id,
                    'title': complaint.title,
                    'content': complaint.content,
                    'status': dict(Complaint.STATUS_CHOICES).get(complaint.status),
                    'tourist_name': complaint.tourist.user.username,
                    'itinerary_name': complaint.itinerary.route.name if complaint.itinerary else None,
                    'created_at': complaint.created_at.isoformat()
                }
                for complaint in complaints
            ]
        }
        return JsonResponse(data)

    return JsonResponse({'success': False, 'error': '请求方法不支持'}, status=405)


@login_required
def update_profile_api(request):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': '请求方法不支持'}, status=405)

    try:
        data = json.loads(request.body)
        user = request.user

        # 更新用户基本信息
        user.username = data.get('username', user.username)
        user.email = data.get('email', user.email)
        user.phone = data.get('phone', user.phone)

        # 如果是旅行社用户，更新旅行社信息
        if user.user_type == 'travel_agency' and hasattr(user, 'travel_agency'):
            travel_agency = user.travel_agency
            travel_agency.agency_name = data.get('agency_name', travel_agency.agency_name)
            travel_agency.license_number = data.get('license_number', travel_agency.license_number)
            travel_agency.address = data.get('address', travel_agency.address)
            travel_agency.save()

        # 处理密码更改
        current_password = data.get('current_password')
        new_password = data.get('new_password')
        if current_password and new_password:
            # 验证当前密码
            if not user.check_password(current_password):
                return JsonResponse({'success': False, 'error': '当前密码不正确'})
            user.set_password(new_password)

        user.save()

        return JsonResponse({'success': True})

    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


@login_required
def upload_profile_image(request):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': '请求方法不支持'}, status=405)

    try:
        if 'profile_image' not in request.FILES:
            return JsonResponse({'success': False, 'error': '没有找到上传的图片'})

        image = request.FILES['profile_image']

        # 检查文件类型
        if not image.name.lower().endswith(('.png', '.jpg', '.jpeg')):
            return JsonResponse({'success': False, 'error': '只支持 PNG、JPG 和 JPEG 格式的图片'})

        # 保存用户图像
        user = request.user

        # 创建存储目录
        profile_dir = os.path.join(settings.MEDIA_ROOT, 'profile_images')
        os.makedirs(profile_dir, exist_ok=True)

        # 生成唯一文件名
        file_ext = os.path.splitext(image.name)[1]
        filename = f"user_{user.id}{file_ext}"
        file_path = os.path.join(profile_dir, filename)

        # 保存文件
        with open(file_path, 'wb+') as destination:
            for chunk in image.chunks():
                destination.write(chunk)

        # 更新用户的图像路径
        profile_image_url = f"/media/profile_images/{filename}"

        # 如果用户有 UserProfile 模型，则更新该模型
        if hasattr(user, 'userprofile'):
            user.userprofile.profile_image = profile_image_url
            user.userprofile.save()
        else:
            # 创建 UserProfile 模型
            from OTA.models import UserProfile
            profile = UserProfile(user=user, profile_image=profile_image_url)
            profile.save()

        return JsonResponse({'success': True, 'image_url': profile_image_url})

    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


@login_required
def get_profile_api(request):
    user = request.user
    data = {
        'username': user.username,
        'email': user.email,
        'phone': user.phone,
        'user_type': user.user_type,
    }

    # 添加用户头像URL
    if hasattr(user, 'userprofile') and user.userprofile.profile_image:
        data['profile_image'] = user.userprofile.profile_image

    # 添加旅行社特定信息
    if user.user_type == 'travel_agency' and hasattr(user, 'travel_agency'):
        data['agency_name'] = user.travel_agency.agency_name
        data['license_number'] = user.travel_agency.license_number
        data['address'] = user.travel_agency.address

    return JsonResponse({'success': True, 'profile': data})


@login_required
def agency_dashboard_stats(request):
    if request.user.user_type != 'travel_agency':
        return JsonResponse({'success': False, 'error': '权限不足'}, status=403)

    try:
        travel_agency = request.user.travel_agency

        # 获取旅行社的路线、导游、预订数量
        routes_count = Route.objects.filter(travel_agency=travel_agency).count()
        guides_count = Guide.objects.filter(travel_agency=travel_agency).count()

        # 获取所有该旅行社的行程
        itineraries = Itinerary.objects.filter(route__travel_agency=travel_agency)

        # 获取预订数量
        bookings_count = Booking.objects.filter(itinerary__in=itineraries).count()

        # 计算总收入
        revenue_total = 0
        for itinerary in itineraries:
            # 假设每个行程有价格属性
            if hasattr(itinerary, 'price'):
                confirmed_bookings = Booking.objects.filter(itinerary=itinerary, status='confirmed').count()
                revenue_total += confirmed_bookings * itinerary.price

        return JsonResponse({
            'success': True,
            'stats': {
                'routes_count': routes_count,
                'guides_count': guides_count,
                'bookings_count': bookings_count,
                'revenue_total': revenue_total
            }
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


@login_required
def agency_guides_detail(request):
    if request.user.user_type != 'travel_agency':
        return JsonResponse({'success': False, 'error': '权限不足'}, status=403)

    try:
        travel_agency = request.user.travel_agency
        guides = Guide.objects.filter(travel_agency=travel_agency).select_related('user')

        guide_data = []
        for guide in guides:
            # 获取导游当前负责的行程
            current_itineraries = Itinerary.objects.filter(
                guide=guide,
                start_date__gte=datetime.now().date(),
                status='active'
            ).select_related('route')

            # 获取导游好评率和投诉次数（示例）
            # 实际实现取决于您的评价和投诉模型
            complaints_count = Complaint.objects.filter(itinerary__guide=guide).count()

            guide_data.append({
                'id': guide.id,
                'name': guide.user.username,
                'guide_id': guide.guide_id,
                'age': 30,  # 假设值，实际应从模型中获取
                'phone': guide.user.phone,
                'email': guide.user.email,
                'rating': 4.5,  # 假设值，实际应从评价计算
                'complaints_count': complaints_count,
                'current_itineraries': [
                    {
                        'id': itinerary.id,
                        'name': itinerary.route.name,
                        'start_date': itinerary.start_date.strftime('%Y-%m-%d')
                    } for itinerary in current_itineraries
                ]
            })

        return JsonResponse({'success': True, 'guides': guide_data})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


@login_required
def agency_bookings_detail(request):
    if request.user.user_type != 'travel_agency':
        return JsonResponse({'success': False, 'error': '权限不足'}, status=403)

    try:
        travel_agency = request.user.travel_agency
        itineraries = Itinerary.objects.filter(route__travel_agency=travel_agency)

        bookings_data = []
        for itinerary in itineraries:
            bookings_count = Booking.objects.filter(itinerary=itinerary).count()

            bookings_data.append({
                'itinerary_id': itinerary.id,
                'itinerary_name': itinerary.route.name,
                'start_date': itinerary.start_date.strftime('%Y-%m-%d'),
                'bookings_count': bookings_count,
                'max_tourists': itinerary.max_tourists
            })

        return JsonResponse({'success': True, 'bookings': bookings_data})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


@login_required
def agency_revenue_detail(request):
    if request.user.user_type != 'travel_agency':
        return JsonResponse({'success': False, 'error': '权限不足'}, status=403)

    try:
        travel_agency = request.user.travel_agency
        itineraries = Itinerary.objects.filter(route__travel_agency=travel_agency)

        revenue_data = []
        for itinerary in itineraries:
            bookings_count = Booking.objects.filter(itinerary=itinerary, status='confirmed').count()
            price = getattr(itinerary, 'price', 0)  # 假设行程有价格字段
            revenue = bookings_count * price

            revenue_data.append({
                'itinerary_id': itinerary.id,
                'itinerary_name': itinerary.route.name,
                'start_date': itinerary.start_date.strftime('%Y-%m-%d'),
                'bookings_count': bookings_count,
                'price': price,
                'revenue': revenue
            })

        return JsonResponse({'success': True, 'revenue': revenue_data})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


@login_required
def agency_itineraries(request):
    if request.user.user_type != 'travel_agency':
        return JsonResponse({'success': False, 'error': '权限不足'}, status=403)

    try:
        travel_agency = request.user.travel_agency

        # 分页参数
        page = int(request.GET.get('page', 1))
        limit = int(request.GET.get('limit', 10))
        offset = (page - 1) * limit

        # 获取行程数据
        itineraries = Itinerary.objects.filter(route__travel_agency=travel_agency).order_by('start_date')
        total_count = itineraries.count()

        # 应用分页
        paginated_itineraries = itineraries[offset:offset + limit]

        itinerary_data = []
        for itinerary in paginated_itineraries:
            bookings_count = Booking.objects.filter(itinerary=itinerary).count()

            itinerary_data.append({
                'id': itinerary.id,
                'name': itinerary.route.name,
                'start_date': itinerary.start_date.strftime('%Y-%m-%d'),
                'guide': itinerary.guide.user.username if itinerary.guide else None,
                'bookings_count': bookings_count,
                'max_tourists': itinerary.max_tourists,
                'status': itinerary.status
            })

        return JsonResponse({
            'success': True,
            'itineraries': itinerary_data,
            'total_count': total_count,
            'page': page,
            'total_pages': (total_count + limit - 1) // limit
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


@login_required
def agency_routes(request):
    if request.user.user_type != 'travel_agency':
        return JsonResponse({'success': False, 'error': '权限不足'}, status=403)

    try:
        travel_agency = request.user.travel_agency

        if request.method == 'GET':
            # 获取旅行社的所有路线
            routes = Route.objects.filter(travel_agency=travel_agency)

            route_data = []
            for route in routes:
                points_count = route.points.count()

                route_data.append({
                    'id': route.id,
                    'name': route.name,
                    'description': route.description,
                    'points_count': points_count,
                    'is_published': route.is_published
                })

            return JsonResponse({'success': True, 'routes': route_data})

        elif request.method == 'POST':
            # 创建新路线
            data = json.loads(request.body)

            name = data.get('name', f'路线 {Route.objects.filter(travel_agency=travel_agency).count() + 1}')
            description = data.get('description', '')
            is_published = data.get('is_published', False)

            route = Route.objects.create(
                name=name,
                description=description,
                travel_agency=travel_agency,
                is_published=is_published
            )

            return JsonResponse({'success': True, 'route_id': route.id})

        else:
            return JsonResponse({'success': False, 'error': '请求方法不支持'}, status=405)

    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


@login_required
def agency_route_detail(request, route_id):
    if request.user.user_type != 'travel_agency':
        return JsonResponse({'success': False, 'error': '权限不足'}, status=403)

    try:
        travel_agency = request.user.travel_agency
        route = get_object_or_404(Route, id=route_id, travel_agency=travel_agency)

        if request.method == 'GET':
            # 获取路线详情
            points = route.points.all().order_by('order')

            points_data = []
            for point in points:
                # 获取点的图片
                images = []
                for img in point.images.all():
                    images.append({
                        'id': img.id,
                        'url': img.image.url
                    })

                points_data.append({
                    'id': point.id,
                    'name': point.name,
                    'latitude': point.latitude,
                    'longitude': point.longitude,
                    'description': point.description,
                    'order': point.order,
                    'images': images
                })

            route_data = {
                'id': route.id,
                'name': route.name,
                'description': route.description,
                'is_published': route.is_published,
                'points': points_data
            }

            return JsonResponse({'success': True, 'route': route_data})

        elif request.method == 'PUT':
            # 更新路线信息
            data = json.loads(request.body)

            route.name = data.get('name', route.name)
            route.description = data.get('description', route.description)
            route.is_published = data.get('is_published', route.is_published)
            route.save()

            return JsonResponse({'success': True})

        elif request.method == 'DELETE':
            # 删除路线
            route.delete()
            return JsonResponse({'success': True})

        else:
            return JsonResponse({'success': False, 'error': '请求方法不支持'}, status=405)

    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


@login_required
def agency_route_points(request, route_id):
    if request.user.user_type != 'travel_agency':
        return JsonResponse({'success': False, 'error': '权限不足'}, status=403)

    try:
        travel_agency = request.user.travel_agency
        route = get_object_or_404(Route, id=route_id, travel_agency=travel_agency)

        if request.method == 'POST':
            # 添加新景点
            data = json.loads(request.body)

            name = data.get('name')
            latitude = data.get('latitude')
            longitude = data.get('longitude')
            description = data.get('description', '')

            # 验证必要字段
            if not name or latitude is None or longitude is None:
                return JsonResponse({'success': False, 'error': '缺少必要字段'})

            # 获取最大序号并加1
            max_order = RoutePoint.objects.filter(route=route).aggregate(models.Max('order'))['order__max'] or -1
            new_order = max_order + 1

            # 创建新景点
            point = RoutePoint.objects.create(
                route=route,
                name=name,
                latitude=latitude,
                longitude=longitude,
                description=description,
                order=new_order
            )

            return JsonResponse({
                'success': True,
                'point_id': point.id,
                'order': point.order
            })

        else:
            return JsonResponse({'success': False, 'error': '请求方法不支持'}, status=405)

    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


@login_required
def agency_route_point_detail(request, route_id, point_id):
    if request.user.user_type != 'travel_agency':
        return JsonResponse({'success': False, 'error': '权限不足'}, status=403)

    try:
        travel_agency = request.user.travel_agency
        route = get_object_or_404(Route, id=route_id, travel_agency=travel_agency)
        point = get_object_or_404(RoutePoint, id=point_id, route=route)

        if request.method == 'PUT':
            # 更新景点信息
            data = json.loads(request.body)

            point.name = data.get('name', point.name)
            point.description = data.get('description', point.description)
            point.save()

            return JsonResponse({'success': True})

        elif request.method == 'DELETE':
            # 删除景点
            point.delete()

            # 重新排序剩余景点
            remaining_points = RoutePoint.objects.filter(route=route).order_by('order')
            for i, p in enumerate(remaining_points):
                p.order = i
                p.save()

            return JsonResponse({'success': True})

        else:
            return JsonResponse({'success': False, 'error': '请求方法不支持'}, status=405)

    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


@login_required
def upload_point_image(request, route_id, point_id):
    if request.user.user_type != 'travel_agency':
        return JsonResponse({'success': False, 'error': '权限不足'}, status=403)

    try:
        travel_agency = request.user.travel_agency
        route = get_object_or_404(Route, id=route_id, travel_agency=travel_agency)
        point = get_object_or_404(RoutePoint, id=point_id, route=route)

        if request.method == 'POST':
            # 处理图片上传
            if 'image' not in request.FILES:
                return JsonResponse({'success': False, 'error': '没有找到上传的图片'})

            image = request.FILES['image']
            point_image = PointImage.objects.create(
                point=point,
                image=image
            )

            return JsonResponse({
                'success': True,
                'image_id': point_image.id,
                'image_url': point_image.image.url
            })

        else:
            return JsonResponse({'success': False, 'error': '请求方法不支持'}, status=405)

    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


@login_required
def delete_point_image(request, route_id, point_id, image_id):
    if request.user.user_type != 'travel_agency' or request.method != 'DELETE':
        return JsonResponse({'success': False, 'error': '权限不足或请求方法不支持'}, status=403)

    try:
        travel_agency = request.user.travel_agency
        route = get_object_or_404(Route, id=route_id, travel_agency=travel_agency)
        point = get_object_or_404(RoutePoint, id=point_id, route=route)
        image = get_object_or_404(PointImage, id=image_id, point=point)

        # 删除物理文件
        if os.path.isfile(image.image.path):
            os.remove(image.image.path)

        # 删除数据库记录
        image.delete()

        return JsonResponse({'success': True})

    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


@login_required
def agency_guides(request):
    if request.user.user_type != 'travel_agency':
        return JsonResponse({'success': False, 'error': '权限不足'}, status=403)

    try:
        travel_agency = request.user.travel_agency

        # 分页参数
        page = int(request.GET.get('page', 1))
        limit = int(request.GET.get('limit', 10))
        offset = (page - 1) * limit

        # 获取该旅行社的导游
        guides = Guide.objects.filter(travel_agency=travel_agency).select_related('user')
        total_count = guides.count()

        # 应用分页
        paginated_guides = guides[offset:offset + limit]

        guides_data = []
        for guide in paginated_guides:
            # 获取导游工资信息
            try:
                salary = guide.salary
                base_salary = salary.base_salary
                bonus_percentage = salary.bonus_percentage
            except GuideSalary.DoesNotExist:
                base_salary = 0
                bonus_percentage = 0

            # 获取导游的行程
            upcoming_itineraries = Itinerary.objects.filter(
                guide=guide,
                start_date__gte=datetime.now().date()
            ).select_related('route').order_by('start_date')[:3]

            # 计算好评率和投诉次数（示例）
            # 实际实现应根据您的评价模型计算
            complaints_count = Complaint.objects.filter(itinerary__guide=guide).count()

            guides_data.append({
                'id': guide.id,
                'user_id': guide.user.id,
                'username': guide.user.username,
                'guide_id': guide.guide_id,
                'email': guide.user.email,
                'phone': guide.user.phone,
                'base_salary': float(base_salary),
                'bonus_percentage': float(bonus_percentage),
                'rating': 4.5,  # 示例值
                'complaints_count': complaints_count,
                'upcoming_itineraries': [
                    {
                        'id': itinerary.id,
                        'name': itinerary.route.name,
                        'start_date': itinerary.start_date.strftime('%Y-%m-%d')
                    } for itinerary in upcoming_itineraries
                ]
            })

        return JsonResponse({
            'success': True,
            'guides': guides_data,
            'total_count': total_count,
            'page': page,
            'total_pages': (total_count + limit - 1) // limit
        })

    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


@login_required
def available_guides(request):
    if request.user.user_type != 'travel_agency':
        return JsonResponse({'success': False, 'error': '权限不足'}, status=403)

    try:
        # 分页参数
        page = int(request.GET.get('page', 1))
        limit = int(request.GET.get('limit', 10))
        offset = (page - 1) * limit

        # 搜索参数
        search_query = request.GET.get('search', '')

        # 获取无归属旅行社的导游
        guides_query = Guide.objects.filter(travel_agency__isnull=True).select_related('user')

        # 应用搜索
        if search_query:
            guides_query = guides_query.filter(
                Q(user__username__icontains=search_query) |
                Q(guide_id__icontains=search_query) |
                Q(user__phone__icontains=search_query)
            )

        total_count = guides_query.count()

        # 应用分页
        paginated_guides = guides_query[offset:offset + limit]

        guides_data = []
        for guide in paginated_guides:
            guides_data.append({
                'id': guide.id,
                'user_id': guide.user.id,
                'username': guide.user.username,
                'guide_id': guide.guide_id,
                'email': guide.user.email,
                'phone': guide.user.phone
            })

        return JsonResponse({
            'success': True,
            'guides': guides_data,
            'total_count': total_count,
            'page': page,
            'total_pages': (total_count + limit - 1) // limit
        })

    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


@login_required
def recruit_guide(request, guide_id):
    if request.user.user_type != 'travel_agency' or request.method != 'POST':
        return JsonResponse({'success': False, 'error': '权限不足或请求方法不支持'}, status=403)

    try:
        travel_agency = request.user.travel_agency
        guide = get_object_or_404(Guide, id=guide_id, travel_agency__isnull=True)

        # 发送聘请通知（实际应用中可能需要更复杂的机制）
        # 这里我们直接修改导游所属旅行社

        guide.travel_agency = travel_agency
        guide.save()

        # 创建默认工资记录
        GuideSalary.objects.create(
            guide=guide,
            base_salary=3000,  # 默认基础工资
            bonus_percentage=5  # 默认提成比例 5%
        )

        # 创建通知消息
        create_notification(
            guide.user,
            f"您已被 {travel_agency.agency_name} 聘请",
            f"{travel_agency.agency_name} 已将您添加为该旅行社的导游。请查看您的导游仪表盘以获取更多信息。"
        )

        return JsonResponse({'success': True})

    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


@login_required
def fire_guide(request, guide_id):
    if request.user.user_type != 'travel_agency' or request.method != 'POST':
        return JsonResponse({'success': False, 'error': '权限不足或请求方法不支持'}, status=403)

    try:
        travel_agency = request.user.travel_agency
        guide = get_object_or_404(Guide, id=guide_id, travel_agency=travel_agency)

        # 检查导游是否有未完成的行程
        has_ongoing_itineraries = Itinerary.objects.filter(
            guide=guide,
            start_date__gte=datetime.now().date(),
            status='active'
        ).exists()

        if has_ongoing_itineraries:
            return JsonResponse({'success': False, 'error': '该导游有未完成的行程，无法开除'})

        # 创建通知消息
        create_notification(
            guide.user,
            f"您已被 {travel_agency.agency_name} 解聘",
            f"{travel_agency.agency_name} 已终止与您的合作关系。如有疑问，请联系旅行社。"
        )

        # 解除导游与旅行社的关系
        guide.travel_agency = None
        guide.save()

        # 删除工资记录
        try:
            guide.salary.delete()
        except:
            pass

        return JsonResponse({'success': True})

    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


@login_required
def update_guide_salary(request, guide_id):
    if request.user.user_type != 'travel_agency' or request.method != 'POST':
        return JsonResponse({'success': False, 'error': '权限不足或请求方法不支持'}, status=403)

    try:
        travel_agency = request.user.travel_agency
        guide = get_object_or_404(Guide, id=guide_id, travel_agency=travel_agency)

        data = json.loads(request.body)
        base_salary = data.get('base_salary')
        bonus_percentage = data.get('bonus_percentage')

        if base_salary is None or bonus_percentage is None:
            return JsonResponse({'success': False, 'error': '缺少必要字段'})

        # 更新或创建工资记录
        salary, created = GuideSalary.objects.get_or_create(
            guide=guide,
            defaults={
                'base_salary': base_salary,
                'bonus_percentage': bonus_percentage
            }
        )

        if not created:
            salary.base_salary = base_salary
            salary.bonus_percentage = bonus_percentage
            salary.save()

        # 创建通知消息
        create_notification(
            guide.user,
            f"薪资方案已更新",
            f"{travel_agency.agency_name} 已更新您的薪资方案。基础工资：¥{base_salary}，提成比例：{bonus_percentage}%"
        )

        return JsonResponse({'success': True})

    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


# 辅助函数：创建通知消息
def create_notification(user, title, content):
    # 这里需要根据您的通知模型进行实现
    # 示例：
    try:
        from OTA.models import Notification
        Notification.objects.create(
            user=user,
            title=title,
            content=content
        )
    except:
        # 如果没有通知模型，可以暂时忽略
        pass


@login_required
def agency_normal_bookings(request):
    if request.user.user_type != 'travel_agency':
        return JsonResponse({'success': False, 'error': '权限不足'}, status=403)

    try:
        travel_agency = request.user.travel_agency

        # 分页参数
        page = int(request.GET.get('page', 1))
        limit = int(request.GET.get('limit', 10))
        offset = (page - 1) * limit

        # 获取常规预订（非候补）
        bookings_query = Booking.objects.filter(
            itinerary__route__travel_agency=travel_agency,
            status__in=['pending', 'confirmed', 'cancelled']
        ).select_related(
            'tourist__user',
            'itinerary__route',
            'itinerary__guide__user'
        ).order_by('-created_at')

        total_count = bookings_query.count()

        # 应用分页
        paginated_bookings = bookings_query[offset:offset + limit]

        bookings_data = []
        for booking in paginated_bookings:
            tourist = booking.tourist
            itinerary = booking.itinerary

            bookings_data.append({
                'id': booking.id,
                'tourist': {
                    'id': tourist.id,
                    'username': tourist.user.username,
                    'phone': tourist.user.phone,
                    'email': tourist.user.email
                },
                'itinerary': {
                    'id': itinerary.id,
                    'name': itinerary.route.name,
                    'start_date': itinerary.start_date.strftime('%Y-%m-%d'),
                    'guide_name': itinerary.guide.user.username if itinerary.guide else None
                },
                'created_at': booking.created_at.strftime('%Y-%m-%d %H:%M'),
                'status': booking.status
            })

        return JsonResponse({
            'success': True,
            'bookings': bookings_data,
            'total_count': total_count,
            'page': page,
            'total_pages': (total_count + limit - 1) // limit
        })

    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


@login_required
def agency_waitlist_bookings(request):
    if request.user.user_type != 'travel_agency':
        return JsonResponse({'success': False, 'error': '权限不足'}, status=403)

    try:
        travel_agency = request.user.travel_agency

        # 分页参数
        page = int(request.GET.get('page', 1))
        limit = int(request.GET.get('limit', 10))
        offset = (page - 1) * limit

        # 获取候补预订
        bookings_query = Booking.objects.filter(
            itinerary__route__travel_agency=travel_agency,
            status='waitlist'
        ).select_related(
            'tourist__user',
            'itinerary__route',
            'itinerary__guide__user'
        ).order_by('-created_at')

        total_count = bookings_query.count()

        # 应用分页
        paginated_bookings = bookings_query[offset:offset + limit]

        bookings_data = []
        for booking in paginated_bookings:
            tourist = booking.tourist
            itinerary = booking.itinerary

            bookings_data.append({
                'id': booking.id,
                'tourist': {
                    'id': tourist.id,
                    'username': tourist.user.username,
                    'phone': tourist.user.phone,
                    'email': tourist.user.email
                },
                'itinerary': {
                    'id': itinerary.id,
                    'name': itinerary.route.name,
                    'start_date': itinerary.start_date.strftime('%Y-%m-%d'),
                    'guide_name': itinerary.guide.user.username if itinerary.guide else None
                },
                'reason': booking.reason,
                'created_at': booking.created_at.strftime('%Y-%m-%d %H:%M')
            })

        return JsonResponse({
            'success': True,
            'bookings': bookings_data,
            'total_count': total_count,
            'page': page,
            'total_pages': (total_count + limit - 1) // limit
        })

    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


@login_required
def agency_approve_booking(request, booking_id):
    if request.user.user_type != 'travel_agency' or request.method != 'POST':
        return JsonResponse({'success': False, 'error': '权限不足或请求方法不支持'}, status=403)

    try:
        travel_agency = request.user.travel_agency
        booking = get_object_or_404(
            Booking,
            id=booking_id,
            status='waitlist',
            itinerary__route__travel_agency=travel_agency
        )

        # 更改状态为已确认
        booking.status = 'confirmed'
        booking.save()

        # 创建通知
        create_notification(
            booking.tourist.user,
            f"预订已确认",
            f"您对{booking.itinerary.route.name}的候补预订申请已获批准。"
        )

        return JsonResponse({'success': True})

    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


@login_required
def agency_reject_booking(request, booking_id):
    if request.user.user_type != 'travel_agency' or request.method != 'POST':
        return JsonResponse({'success': False, 'error': '权限不足或请求方法不支持'}, status=403)

    try:
        travel_agency = request.user.travel_agency
        booking = get_object_or_404(
            Booking,
            id=booking_id,
            status__in=['waitlist', 'pending'],
            itinerary__route__travel_agency=travel_agency
        )

        # 更改状态为已取消
        booking.status = 'cancelled'
        booking.save()

        # 创建通知
        create_notification(
            booking.tourist.user,
            f"预订已拒绝",
            f"您对{booking.itinerary.route.name}的预订申请未获批准。"
        )

        return JsonResponse({'success': True})

    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


@login_required
def agency_confirm_booking(request, booking_id):
    if request.user.user_type != 'travel_agency' or request.method != 'POST':
        return JsonResponse({'success': False, 'error': '权限不足或请求方法不支持'}, status=403)

    try:
        travel_agency = request.user.travel_agency
        booking = get_object_or_404(
            Booking,
            id=booking_id,
            status='pending',
            itinerary__route__travel_agency=travel_agency
        )

        # 更改状态为已确认
        booking.status = 'confirmed'
        booking.save()

        # 创建通知
        create_notification(
            booking.tourist.user,
            f"预订已确认",
            f"您对{booking.itinerary.route.name}的预订申请已确认。"
        )

        return JsonResponse({'success': True})

    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


@login_required
def agency_booking_detail(request, booking_id):
    if request.user.user_type != 'travel_agency':
        return JsonResponse({'success': False, 'error': '权限不足'}, status=403)

    try:
        travel_agency = request.user.travel_agency
        booking = get_object_or_404(
            Booking,
            id=booking_id,
            itinerary__route__travel_agency=travel_agency
        )

        tourist = booking.tourist
        itinerary = booking.itinerary

        booking_data = {
            'id': booking.id,
            'tourist': {
                'id': tourist.id,
                'username': tourist.user.username,
                'phone': tourist.user.phone,
                'email': tourist.user.email
            },
            'itinerary': {
                'id': itinerary.id,
                'name': itinerary.route.name,
                'description': itinerary.route.description,
                'start_date': itinerary.start_date.strftime('%Y-%m-%d'),
                'guide_name': itinerary.guide.user.username if itinerary.guide else None
            },
            'status': booking.status,
            'reason': booking.reason,
            'created_at': booking.created_at.strftime('%Y-%m-%d %H:%M'),
            'updated_at': booking.updated_at.strftime('%Y-%m-%d %H:%M')
        }

        return JsonResponse({
            'success': True,
            'booking': booking_data
        })

    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


@login_required
def agency_manage_itineraries(request):
    if request.user.user_type != 'travel_agency':
        return JsonResponse({'success': False, 'error': '权限不足'}, status=403)

    try:
        travel_agency = request.user.travel_agency

        if request.method == 'GET':
            # 分页参数
            page = int(request.GET.get('page', 1))
            limit = int(request.GET.get('limit', 10))
            offset = (page - 1) * limit

            # 获取行程
            itineraries = Itinerary.objects.filter(
                route__travel_agency=travel_agency
            ).select_related('route', 'guide__user').order_by('-start_date')

            total_count = itineraries.count()

            # 应用分页
            paginated_itineraries = itineraries[offset:offset + limit]

            itinerary_data = []
            for itinerary in paginated_itineraries:
                # 获取预订数
                bookings_count = Booking.objects.filter(
                    itinerary=itinerary,
                    status='confirmed'
                ).count()

                itinerary_data.append({
                    'id': itinerary.id,
                    'name': itinerary.route.name,
                    'start_date': itinerary.start_date.strftime('%Y-%m-%d'),
                    'guide': {
                        'id': itinerary.guide.id if itinerary.guide else None,
                        'name': itinerary.guide.user.username if itinerary.guide else None
                    },
                    'bookings_count': bookings_count,
                    'max_tourists': itinerary.max_tourists,
                    'status': itinerary.status,
                    'price': float(itinerary.price) if hasattr(itinerary, 'price') else 0
                })

            return JsonResponse({
                'success': True,
                'itineraries': itinerary_data,
                'total_count': total_count,
                'page': page,
                'total_pages': (total_count + limit - 1) // limit
            })

        elif request.method == 'POST':
            # 创建新行程
            data = json.loads(request.body)

            # 必要字段
            route_id = data.get('route_id')
            start_date = data.get('start_date')
            if not route_id or not start_date:
                return JsonResponse({'success': False, 'error': '缺少必要字段'})

            # 获取路线
            try:
                route = Route.objects.get(id=route_id, travel_agency=travel_agency)
            except Route.DoesNotExist:
                return JsonResponse({'success': False, 'error': '路线不存在'})

            # 可选字段
            guide_id = data.get('guide_id')
            guide = None
            if guide_id:
                try:
                    guide = Guide.objects.get(id=guide_id, travel_agency=travel_agency)
                except Guide.DoesNotExist:
                    return JsonResponse({'success': False, 'error': '导游不存在'})

            max_tourists = data.get('max_tourists', 20)
            is_published = data.get('is_published', False)
            price = data.get('price', 0)

            # 创建行程
            itinerary = Itinerary.objects.create(
                route=route,
                guide=guide,
                start_date=start_date,
                max_tourists=max_tourists,
                status='active' if is_published else 'draft',
                price=price
            )

            return JsonResponse({
                'success': True,
                'itinerary_id': itinerary.id
            })

        else:
            return JsonResponse({'success': False, 'error': '请求方法不支持'}, status=405)

    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


@login_required
def agency_itinerary_detail(request, itinerary_id):
    if request.user.user_type != 'travel_agency':
        return JsonResponse({'success': False, 'error': '权限不足'}, status=403)

    try:
        travel_agency = request.user.travel_agency
        itinerary = get_object_or_404(
            Itinerary,
            id=itinerary_id,
            route__travel_agency=travel_agency
        )

        if request.method == 'GET':
            # 获取行程详情
            route = itinerary.route
            points = route.points.all().order_by('order')

            # 获取预订
            bookings = Booking.objects.filter(
                itinerary=itinerary,
                status='confirmed'
            ).select_related('tourist__user')

            points_data = []
            for point in points:
                # 获取点的图片
                images = []
                for img in point.images.all():
                    images.append({
                        'id': img.id,
                        'url': img.image.url
                    })

                points_data.append({
                    'id': point.id,
                    'name': point.name,
                    'latitude': point.latitude,
                    'longitude': point.longitude,
                    'description': point.description,
                    'order': point.order,
                    'images': images
                })

            bookings_data = []
            for booking in bookings:
                tourist = booking.tourist
                bookings_data.append({
                    'id': booking.id,
                    'tourist': {
                        'id': tourist.id,
                        'username': tourist.user.username,
                        'phone': tourist.user.phone,
                        'email': tourist.user.email
                    },
                    'created_at': booking.created_at.strftime('%Y-%m-%d %H:%M')
                })

            # 等候名单
            waitlist = Booking.objects.filter(
                itinerary=itinerary,
                status='waitlist'
            ).count()

            itinerary_data = {
                'id': itinerary.id,
                'name': route.name,
                'description': route.description,
                'start_date': itinerary.start_date.strftime('%Y-%m-%d'),
                'guide': {
                    'id': itinerary.guide.id if itinerary.guide else None,
                    'name': itinerary.guide.user.username if itinerary.guide else None
                },
                'max_tourists': itinerary.max_tourists,
                'bookings_count': bookings.count(),
                'waitlist_count': waitlist,
                'status': itinerary.status,
                'price': float(itinerary.price) if hasattr(itinerary, 'price') else 0,
                'points': points_data,
                'tourists': bookings_data
            }

            return JsonResponse({
                'success': True,
                'itinerary': itinerary_data
            })

        elif request.method == 'PUT':
            # 更新行程
            data = json.loads(request.body)

            # 可更新字段
            if 'guide_id' in data:
                guide_id = data.get('guide_id')
                if guide_id:
                    try:
                        guide = Guide.objects.get(id=guide_id, travel_agency=travel_agency)
                        itinerary.guide = guide
                    except Guide.DoesNotExist:
                        return JsonResponse({'success': False, 'error': '导游不存在'})
                else:
                    itinerary.guide = None

            if 'start_date' in data:
                itinerary.start_date = data.get('start_date')

            if 'max_tourists' in data:
                itinerary.max_tourists = data.get('max_tourists')

            if 'status' in data:
                itinerary.status = data.get('status')

            if 'price' in data:
                itinerary.price = data.get('price')

            # 保存更改
            itinerary.save()

            return JsonResponse({'success': True})

        elif request.method == 'DELETE':
            # 检查是否有已确认的预订
            has_confirmed_bookings = Booking.objects.filter(
                itinerary=itinerary,
                status='confirmed'
            ).exists()

            if has_confirmed_bookings:
                return JsonResponse({
                    'success': False,
                    'error': '此行程已有确认的预订，无法删除'
                })

            # 删除行程
            itinerary.delete()

            return JsonResponse({'success': True})

        else:
            return JsonResponse({'success': False, 'error': '请求方法不支持'}, status=405)

    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


@login_required
def agency_available_routes(request):
    if request.user.user_type != 'travel_agency':
        return JsonResponse({'success': False, 'error': '权限不足'}, status=403)

    try:
        travel_agency = request.user.travel_agency

        # 获取旅行社的所有已发布路线
        routes = Route.objects.filter(
            travel_agency=travel_agency,
            is_published=True
        )

        routes_data = []
        for route in routes:
            # 获取路线点数
            points_count = route.points.count()

            routes_data.append({
                'id': route.id,
                'name': route.name,
                'description': route.description,
                'points_count': points_count
            })

        return JsonResponse({
            'success': True,
            'routes': routes_data
        })

    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


@login_required
def agency_available_guides(request):
    if request.user.user_type != 'travel_agency':
        return JsonResponse({'success': False, 'error': '权限不足'}, status=403)

    try:
        travel_agency = request.user.travel_agency

        # 获取旅行社的所有导游
        guides = Guide.objects.filter(
            travel_agency=travel_agency
        ).select_related('user')

        guides_data = []
        for guide in guides:
            guides_data.append({
                'id': guide.id,
                'name': guide.user.username,
                'guide_id': guide.guide_id
            })

        return JsonResponse({
            'success': True,
            'guides': guides_data
        })

    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


@login_required
def agency_cancel_itinerary(request, itinerary_id):
    if request.user.user_type != 'travel_agency' or request.method != 'POST':
        return JsonResponse({'success': False, 'error': '权限不足或请求方法不支持'}, status=403)

    try:
        travel_agency = request.user.travel_agency
        itinerary = get_object_or_404(
            Itinerary,
            id=itinerary_id,
            route__travel_agency=travel_agency
        )

        # 更改行程状态为已取消
        itinerary.status = 'cancelled'
        itinerary.save()

        # 取消所有预订
        bookings = Booking.objects.filter(
            itinerary=itinerary,
            status__in=['confirmed', 'pending', 'waitlist']
        )

        bookings.update(status='cancelled')

        # 通知游客
        for booking in bookings:
            create_notification(
                booking.tourist.user,
                f"行程已取消",
             f"行程“{itinerary.route.name}”已被旅行社取消。如有疑问，请联系旅行社。"
            )

            return JsonResponse({'success': True})

    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


@login_required
def agency_revenue_statistics(request):
    if request.user.user_type != 'travel_agency':
        return JsonResponse({'success': False, 'error': '权限不足'}, status=403)

    try:
        travel_agency = request.user.travel_agency

        # 获取最近12个月的数据
        end_date = datetime.now().date()
        start_date = end_date.replace(year=end_date.year - 1 if end_date.month == 12 else end_date.year,
                                      month=end_date.month + 1 if end_date.month < 12 else 1)

        # 按月统计收入
        monthly_revenue = []
        current_date = start_date

        while current_date <= end_date:
            month_start = current_date.replace(day=1)
            if current_date.month == 12:
                next_month = current_date.replace(year=current_date.year + 1, month=1, day=1)
            else:
                next_month = current_date.replace(month=current_date.month + 1, day=1)

            # 获取该月出发的行程
            itineraries = Itinerary.objects.filter(
                route__travel_agency=travel_agency,
                start_date__gte=month_start,
                start_date__lt=next_month
            )

            # 计算收入
            month_revenue = 0
            for itinerary in itineraries:
                if hasattr(itinerary, 'price'):
                    confirmed_bookings = Booking.objects.filter(
                        itinerary=itinerary,
                        status='confirmed'
                    ).count()
                    month_revenue += confirmed_bookings * itinerary.price

            monthly_revenue.append({
                'month': current_date.strftime('%Y-%m'),
                'revenue': float(month_revenue)
            })

            # 移动到下一个月
            current_date = next_month

        return JsonResponse({
            'success': True,
            'monthly_revenue': monthly_revenue
        })

    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


@login_required
def agency_popular_routes(request):
    if request.user.user_type != 'travel_agency':
        return JsonResponse({'success': False, 'error': '权限不足'}, status=403)

    try:
        travel_agency = request.user.travel_agency

        # 获取路线，按预订数排序
        routes_data = []

        routes = Route.objects.filter(travel_agency=travel_agency)
        for route in routes:
            # 获取路线的所有行程
            itineraries = Itinerary.objects.filter(route=route)

            # 计算确认的预订数量
            bookings_count = Booking.objects.filter(
                itinerary__in=itineraries,
                status='confirmed'
            ).count()

            routes_data.append({
                'id': route.id,
                'name': route.name,
                'bookings_count': bookings_count
            })

        # 按预订数量排序
        routes_data.sort(key=lambda x: x['bookings_count'], reverse=True)

        # 只返回前10个
        return JsonResponse({
            'success': True,
            'popular_routes': routes_data[:10]
        })

    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


@login_required
def agency_tourist_sources(request):
    if request.user.user_type != 'travel_agency':
        return JsonResponse({'success': False, 'error': '权限不足'}, status=403)

    try:
        travel_agency = request.user.travel_agency

        # 示例数据，实际应该根据游客的地理信息进行统计
        # 这里假设已有一些城市数据
        sources_data = [
            {'city': '北京', 'count': 120},
            {'city': '上海', 'count': 98},
            {'city': '广州', 'count': 82},
            {'city': '深圳', 'count': 75},
            {'city': '杭州', 'count': 63},
            {'city': '成都', 'count': 58},
            {'city': '武汉', 'count': 45},
            {'city': '西安', 'count': 42},
            {'city': '南京', 'count': 39},
            {'city': '重庆', 'count': 35},
        ]

        return JsonResponse({
            'success': True,
            'tourist_sources': sources_data
        })

    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


@login_required
def agency_guide_performance(request):
    if request.user.user_type != 'travel_agency':
        return JsonResponse({'success': False, 'error': '权限不足'}, status=403)

    try:
        travel_agency = request.user.travel_agency

        # 获取所有导游
        guides = Guide.objects.filter(travel_agency=travel_agency).select_related('user')

        guides_data = []
        for guide in guides:
            # 获取导游负责的行程数量
            itineraries_count = Itinerary.objects.filter(guide=guide).count()

            # 示例数据，实际应该根据评价计算
            # 这里假设有一些评价数据
            avg_rating = round(4 + random.random(), 1)  # 模拟4-5之间的评分

            # 获取投诉数量
            complaints_count = Complaint.objects.filter(itinerary__guide=guide).count()

            # 计算投诉率
            complaint_rate = round(complaints_count / max(itineraries_count, 1) * 100, 1)

            guides_data.append({
                'id': guide.id,
                'name': guide.user.username,
                'itineraries_count': itineraries_count,
                'rating': avg_rating,
                'complaint_rate': complaint_rate,
                'avg_score': avg_rating
            })

        return JsonResponse({
            'success': True,
            'guides_performance': guides_data
        })

    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})
