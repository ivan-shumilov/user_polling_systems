from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from ..models import Poll


class PollTest(TestCase):
    fixtures = ['fixtures/polls.Poll.json']

    def test_polls(self):
        client = APIClient()
        response = client.get('/api/v1/polls/')
        self.assertEqual(response.status_code, 200)
