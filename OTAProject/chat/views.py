# OTAProject/chat/views.py
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from OTA.models import Guide
from .models import ChatRoom, ChatMessage


@login_required
def chat_contacts(request):
    if request.user.user_type != 'travel_agency':
        return JsonResponse({'error': '未授权'}, status=403)

    agency = request.user.travel_agency
    guides = Guide.objects.filter(travel_agency=agency)

    guide_list = [{'id': guide.id, 'name': guide.user.username} for guide in guides]

    return JsonResponse({
        'guides': guide_list
    })


@login_required
def chat_history(request):
    if request.user.user_type != 'travel_agency':
        return JsonResponse({'error': '未授权'}, status=403)

    chat_id = request.GET.get('chat_id')

    if not chat_id:
        return JsonResponse({'error': 'Missing chat_id parameter'}, status=400)

    # 根据chat_id查找对应的room_id
    room_id = None
    if chat_id == 'agency-group':
        room_id = 'agency_bureau_group'

    if not room_id:
        return JsonResponse({'messages': []})

    # 查询聊天记录
    try:
        room = ChatRoom.objects.get(room_id=room_id)
        messages = ChatMessage.objects.filter(room=room).order_by('timestamp')

        message_list = []
        for msg in messages:
            sender_name = msg.sender.username
            if msg.sender.user_type == 'travel_agency':
                try:
                    sender_name = msg.sender.travel_agency.agency_name
                except:
                    pass

            message_list.append({
                'sender': sender_name,
                'message': msg.content,
                'timestamp': msg.timestamp.isoformat()
            })

        return JsonResponse({'messages': message_list})
    except ChatRoom.DoesNotExist:
        return JsonResponse({'messages': []})