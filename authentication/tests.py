from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth.models import User

class AuthTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.register_url = reverse('signup')  # Assuming the name is 'register' (need to verify urls)
        self.login_url = reverse('login')        # Assuming the name is 'login'
        
        self.user_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "Password123"
        }
        self.user = User.objects.create_user(**self.user_data)

    def test_register_success(self):
        data = {
            "username": "newuser",
            "email": "new@example.com",
            "password": "Password123"
        }
        response = self.client.post("/api/auth/signup/", data) # using direct url if name check fails
        
        # Check if the url naming is different, I'll assume direct path first or look it up.
        # Let's inspect urls.py first if this fails, but direct path is safer for now based on settings.
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['status'], 'success')
        self.assertIn('tokens', response.data)

    def test_login_success(self):
        data = {
            "username": "testuser",
            "password": "Password123"
        }
        response = self.client.post("/api/auth/login/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'success')

    def test_login_invalid_credentials(self):
        data = {
            "username": "testuser",
            "password": "WrongPassword"
        }
        response = self.client.post("/api/auth/login/", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['status'], 'error')

    def test_login_inactive_user(self):
        self.user.is_active = False
        self.user.save()
        data = {
            "username": "testuser",
            "password": "Password123"
        }
        response = self.client.post("/api/auth/login/", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("not active", str(response.data))
