from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from ..models import Poll
from users.models import User
from rest_framework.authtoken.models import Token


class CreatePollTest(TestCase):

    def setUp(self):
        self.email = 'test.test@test.com'
        self.password = '123456789'
        User.objects.all().delete()
        Poll.objects.all().delete()

    def test_create_poll(self):
        client = APIClient()
        user = User.objects.create_superuser(email=self.email, password=self.password)
        token = Token.objects.create(user=user)
        client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')

        data = {'name': 'poll test1', 'description': 'description1', 'date_start': '2021-05-01 11:11',
                'date_finish': '2021-06-01 11:11'}
        response = client.post(reverse('admin_polls-list'), data)
        self.assertEqual(response.status_code, 201)

    def test_wrong_create_poll(self):
        client = APIClient()
        user = User.objects.create_superuser(email=self.email, password=self.password)
        token = Token.objects.create(user=user)
        client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')

        data = {'name': 'poll test1', 'description': 'description1'}
        response = client.post(reverse('admin_polls-list'), data)
        self.assertEqual(response.status_code, 400)

    def test_wrong_without_rulls_create_poll(self):
        client = APIClient()
        user = User.objects.create_superuser(email=self.email, password=self.password)
        user.is_staff = False
        user.save()
        token = Token.objects.create(user=user)
        client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')

        data = {'name': 'poll test1', 'description': 'description1', 'date_start': '2021-05-01 11:11',
                'date_finish': '2021-06-01 11:11'}
        response = client.post(reverse('admin_polls-list'), data)
        self.assertEqual(response.status_code, 403)


class PollTest(TestCase):
    fixtures = ['fixtures/polls.Poll.json']

    def setUp(self):
        self.email = 'test.test@test.com'
        self.password = '123456789'
        User.objects.all().delete()
        Poll.objects.all().delete()

    def test_polls(self):
        client = APIClient()
        user = User.objects.create_superuser(email=self.email, password=self.password)
        token = Token.objects.create(user=user)
        client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')

        response = client.get(reverse('admin_polls-list'))
        self.assertEqual(response.status_code, 200)

    def test_wrong_without_rulls_polls(self):
        client = APIClient()
        user = User.objects.create_superuser(email=self.email, password=self.password)
        user.is_staff = False
        user.save()
        token = Token.objects.create(user=user)
        client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')

        response = client.get(reverse('admin_polls-list'))
        self.assertEqual(response.status_code, 403)


class DeletePollTest(TestCase):

    def setUp(self):
        self.email = 'test.test@test.com'
        self.password = '123456789'
        User.objects.all().delete()
        Poll.objects.all().delete()

    def test_delete_poll(self):
        client = APIClient()
        user = User.objects.create_superuser(email=self.email, password=self.password)
        token = Token.objects.create(user=user)
        client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')
        data = {'name': 'poll test1', 'description': 'description1', 'date_start': '2021-05-01 11:11',
                'date_finish': '2021-06-01 11:11'}
        poll = Poll.objects.create(**data)
        self.assertEqual(poll.name, data['name'])

        response = client.delete(f"{reverse('admin_polls-list')}{poll.id}/")
        self.assertEqual(response.status_code, 204)

    def test_wrong_delete_poll_without_rulls(self):
        client = APIClient()
        user = User.objects.create_superuser(email=self.email, password=self.password)
        user.is_staff = False
        user.save()
        token = Token.objects.create(user=user)
        client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')
        data = {'name': 'poll test1', 'description': 'description1', 'date_start': '2021-05-01 11:11',
                'date_finish': '2021-06-01 11:11'}
        poll = Poll.objects.create(**data)
        self.assertEqual(poll.name, data['name'])

        response = client.delete(f"{reverse('admin_polls-list')}{poll.id}/")
        self.assertEqual(response.status_code, 403)

    def test_wrong_delete_poll_not_found(self):
        client = APIClient()
        user = User.objects.create_superuser(email=self.email, password=self.password)
        token = Token.objects.create(user=user)
        client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')

        response = client.delete(f"{reverse('admin_polls-list')}100/")
        self.assertEqual(response.status_code, 404)
