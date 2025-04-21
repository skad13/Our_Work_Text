from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from OTA.models import Role, UserProfile

class Command(BaseCommand):
    help = 'Creates a default authority user'

    def handle(self, *args, **options):
        username = '文旅局'
        password = '12345678'
        email = '2273387741@qq.com'
        role_name = 'authority'

        # 检查用户是否存在
        if User.objects.filter(username=username).exists():
            self.stdout.write(self.style.SUCCESS(f'Authority user "{username}" already exists'))
            return

        # 获取或创建角色
        role, created = Role.objects.get_or_create(name=role_name)

        # 创建用户
        user = User.objects.create_user(username=username, password=password, email=email)

        # 创建用户资料
        UserProfile.objects.create(user=user, role=role)

        self.stdout.write(self.style.SUCCESS(f'Successfully created authority user "{username}"'))