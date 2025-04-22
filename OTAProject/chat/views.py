# OTAProject/chat/views.py
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from OTA.models import Guide


@login_required
def chat_contacts_api(request):
    if request.user.user_type == 'travel_agency':
        # 旅行社能看到自己的导游
        guides = Guide.objects.filter(travel_agency=request.user.travel_agency)
        contacts = [
            {
                'id': guide.id,
                'name': guide.user.username,
                'type': 'guide'
            }
            for guide in guides
        ]

        # 添加文旅局群组
        contacts.insert(0, {
            'id': 'bureau_group',
            'name': '文旅局与旅行社群组',
            'type': 'group'
        })

        return JsonResponse({'contacts': contacts})

    # 其他用户角色的联系人逻辑可以后续添加

    return JsonResponse({'contacts': []})


@login_required
def chat_history_api(request):
    chat_id = request.GET.get('chat_id')
    if not chat_id:
        return JsonResponse({'messages': []})

    # 简化版，实际实现应从数据库获取聊天记录
    messages = [
        {
            'sender': '系统',
            'message': '欢迎使用聊天系统，这是一个简化版的聊天记录示例。',
            'timestamp': '2023-01-01T12:00:00'
        }
    ]

    return JsonResponse({'messages': messages})