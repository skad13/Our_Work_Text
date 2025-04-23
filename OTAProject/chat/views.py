from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import ensure_csrf_cookie
import json
from datetime import datetime

from OTA.models import User, ChatRoom, ChatMessage, ChatRoomMember, Notification


@login_required
def get_chat_rooms(request):
    user = request.user

    # 获取用户所在的聊天室
    room_memberships = ChatRoomMember.objects.filter(user=user).select_related('room')

    rooms_data = []
    for membership in room_memberships:
        room = membership.room

        # 获取最后一条消息
        last_message = ChatMessage.objects.filter(room=room).order_by('-created_at').first()

        # 获取未读消息数量
        # 实际实现应该记录用户上次读取每个聊天室的时间，然后计算之后的消息数量
        # 这里简单示例，假设所有消息都已读
        unread_count = 0

        # 获取聊天室名称，对于非群聊，显示对方名称
        if not room.is_group:
            # 找出对方用户
            other_member = ChatRoomMember.objects.filter(room=room).exclude(user=user).first()
            display_name = other_member.user.username if other_member else room.name
        else:
            display_name = room.name

        rooms_data.append({
            'id': room.id,
            'name': display_name,
            'is_group': room.is_group,
            'last_message': {
                'content': last_message.content if last_message else None,
                'sender_name': last_message.sender.username if last_message else None,
                'time': last_message.created_at.strftime('%Y-%m-%d %H:%M') if last_message else None
            },
            'unread_count': unread_count
        })

    return JsonResponse({
        'success': True,
        'rooms': rooms_data
    })


@login_required
def get_chat_messages(request, room_id):
    user = request.user

    # 检查用户是否在聊天室中
    membership = get_object_or_404(ChatRoomMember, room_id=room_id, user=user)

    # 获取消息，分页参数
    page = int(request.GET.get('page', 1))
    limit = int(request.GET.get('limit', 50))
    offset = (page - 1) * limit

    # 获取消息
    messages = ChatMessage.objects.filter(room_id=room_id).order_by('-created_at')[offset:offset + limit]

    # 获取总消息数
    total_count = ChatMessage.objects.filter(room_id=room_id).count()

    messages_data = []
    for message in messages:
        messages_data.append({
            'id': message.id,
            'sender_id': message.sender.id,
            'sender_name': message.sender.username,
            'content': message.content,
            'is_my_message': message.sender == user,
            'time': message.created_at.strftime('%Y-%m-%d %H:%M')
        })

    # 逆序消息以便按时间顺序显示（最新的在底部）
    messages_data.reverse()

    return JsonResponse({
        'success': True,
        'room_name': membership.room.name,
        'is_group': membership.room.is_group,
        'messages': messages_data,
        'total_count': total_count,
        'page': page,
        'total_pages': (total_count + limit - 1) // limit
    })


@login_required
def send_message(request, room_id):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': '请求方法不支持'}, status=405)

    user = request.user

    # 检查用户是否在聊天室中
    membership = get_object_or_404(ChatRoomMember, room_id=room_id, user=user)

    try:
        data = json.loads(request.body)
        content = data.get('content')

        if not content or content.strip() == '':
            return JsonResponse({'success': False, 'error': '消息内容不能为空'})

        # 创建新消息
        message = ChatMessage.objects.create(
            room_id=room_id,
            sender=user,
            content=content
        )

        # 在实际实现中，这里应该触发WebSocket消息通知其他用户

        return JsonResponse({
            'success': True,
            'message': {
                'id': message.id,
                'sender_id': user.id,
                'sender_name': user.username,
                'content': message.content,
                'is_my_message': True,
                'time': message.created_at.strftime('%Y-%m-%d %H:%M')
            }
        })

    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


@login_required
def create_chat_room(request):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': '请求方法不支持'}, status=405)

    user = request.user

    try:
        data = json.loads(request.body)

        is_group = data.get('is_group', False)
        name = data.get('name')
        member_ids = data.get('member_ids', [])

        if not is_group and len(member_ids) != 1:
            return JsonResponse({'success': False, 'error': '私聊必须且只能有一个聊天对象'})

        if is_group and not name:
            return JsonResponse({'success': False, 'error': '群聊必须提供名称'})

        # 创建聊天室
        room = ChatRoom.objects.create(
            name=name,
            is_group=is_group
        )

        # 添加创建者为成员
        ChatRoomMember.objects.create(
            room=room,
            user=user,
            is_admin=True
        )

        # 添加其他成员
        for member_id in member_ids:
            try:
                member = User.objects.get(id=member_id)
                ChatRoomMember.objects.create(
                    room=room,
                    user=member
                )
            except User.DoesNotExist:
                # 忽略不存在的用户
                pass

        return JsonResponse({
            'success': True,
            'room_id': room.id
        })

    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


@login_required
def get_notifications(request):
    user = request.user

    # 分页参数
    page = int(request.GET.get('page', 1))
    limit = int(request.GET.get('limit', 10))
    offset = (page - 1) * limit

    # 获取通知
    notifications = Notification.objects.filter(user=user).order_by('-created_at')

    total_count = notifications.count()
    paginated_notifications = notifications[offset:offset + limit]

    notifications_data = []
    for notification in paginated_notifications:
        notifications_data.append({
            'id': notification.id,
            'title': notification.title,
            'content': notification.content,
            'is_read': notification.is_read,
            'created_at': notification.created_at.strftime('%Y-%m-%d %H:%M')
        })

    # 统计未读通知数量
    unread_count = notifications.filter(is_read=False).count()

    return JsonResponse({
        'success': True,
        'notifications': notifications_data,
        'unread_count': unread_count,
        'total_count': total_count,
        'page': page,
        'total_pages': (total_count + limit - 1) // limit
    })


@login_required
def mark_notification_as_read(request, notification_id):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': '请求方法不支持'}, status=405)

    user = request.user

    try:
        notification = get_object_or_404(Notification, id=notification_id, user=user)
        notification.is_read = True
        notification.save()

        return JsonResponse({'success': True})

    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


@login_required
def mark_all_notifications_as_read(request):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': '请求方法不支持'}, status=405)

    user = request.user

    try:
        Notification.objects.filter(user=user, is_read=False).update(is_read=True)

        return JsonResponse({'success': True})

    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})