from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from .models import User
from rest_framework.authtoken.models import Token


class SignInTest(TestCase):

    def setUp(self):
        self.email = 'test.test@test.com'
        self.password = '123456789'
        self.unknown_email = 'test@test.test'
        self.unknown_password = 'testtesst'
        User.objects.all().delete()

    def test_signin_success(self):
        client = APIClient()
        data = {'email': self.email, 'password': self.password}
        user = User.objects.create_superuser(email=self.email, password=self.password)
        Token.objects.create(user=user)
        response = client.post(reverse('sign_in-list'), data)
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.json()['token'], '')

    def test_wrong_signin_without_token(self):
        client = APIClient()
        data = {'email': self.email, 'password': self.password}
        User.objects.create_superuser(email=self.email, password=self.password)
        response = client.post(reverse('sign_in-list'), data)
        self.assertEqual(response.status_code, 400)

    def test_wrong_signin_unknown_email(self):
        client = APIClient()
        user = User.objects.create_superuser(email=self.email, password=self.password)
        Token.objects.create(user=user)
        data = {'email': self.unknown_email, 'password': self.password}
        response = client.post(reverse('sign_in-list'), data)
        self.assertEqual(response.status_code, 400)

    def test_wrong_signin_unknown_password(self):
        client = APIClient()
        user = User.objects.create_superuser(email=self.email, password=self.password)
        Token.objects.create(user=user)
        data = {'email': self.email, 'password': self.unknown_password}
        response = client.post(reverse('sign_in-list'), data)
        self.assertEqual(response.status_code, 400)
