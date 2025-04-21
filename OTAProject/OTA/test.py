from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from .models import Role, UserProfile

class UserRegistrationTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.register_url = reverse('OTA:register')  # 添加 OTA: 前缀
        self.login_url = reverse('OTA:login')    # 添加 OTA: 前缀
        self.tourist_role, _ = Role.objects.get_or_create(name='tourist')

    def test_register_user(self):
        data = {
            'username': 'newtestuser',
            'password': 'testpassword',
            'email': 'test@example.com',
            'role': 'tourist'
        }
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get(username='newtestuser').email, 'test@example.com')

    def test_login_user(self):
        # 首先注册用户
        data = {
            'username': 'testuser',
            'password': 'testpassword',
            'email': 'test@example.com',
            'role': 'tourist'
        }
        self.client.post(self.register_url, data, format='json')

        # 然后尝试登录
        login_data = {
            'username': 'testuser',
            'password': 'testpassword'
        }
        response = self.client.post(self.login_url, login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)