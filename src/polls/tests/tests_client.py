from django.test import TestCase
from rest_framework.test import APIClient
from ..enum import TypePoll


class UserPollsTest(TestCase):
    fixtures = ['fixtures/polls.Poll.json', 'fixtures/polls.Questions.json', 'fixtures/polls.OptionTheQuestion.json']

    def setUp(self):
        self.user_id = 1
        self.other_user_id = 2

    def test_available_polls(self, text_poll_id, choice_poll_id, completed_poll_id):
        client = APIClient()
        response = client.get('/api/v1/polls/')
        self.assertEqual(response.status_code, 200)
        polls = response.json()
        poll_IDs = [p['id'] for p in polls]
        self.assertIn(text_poll_id, poll_IDs)
        self.assertIn(choice_poll_id, poll_IDs)
        self.assertIn(completed_poll_id, poll_IDs)

    def test_submit_closed_poll(self, completed_poll_id):
        client = APIClient()
        response = client.get(f'/api/v1/polls/{completed_poll_id}')
        self.assertEqual(response.status_code, 404)
        submit_data = {
            'userId': self.user_id,
            'answers': {}
        }
        response = client.get(f'/api/v1/polls/{completed_poll_id}', json=submit_data)
        self.assertEqual(response.status_code, 404)

    def test_submit_uncomplete_poll(self, text_poll_id):
        client = APIClient()
        response = client.get(f'/api/v1/polls/{text_poll_id}')
        self.assertEqual(response.status_code, 200)
        poll = response.json()
        submit_data = {
            'userId': self.user_id,
            'answers': {}
        }
        question = poll['questions'][0]
        submit_data['answers'][str(question['id'])] = 'Test'

        response = client.get(f'/api/v1/polls/{submit_data}', json=submit_data)
        self.assertEqual(response.status_code, 400)

    def test_submit_text_poll(self, text_poll_id):
        client = APIClient()
        response = client.get(f'/api/v1/polls/{text_poll_id}')
        self.assertEqual(response.status_code, 200)
        poll = response.json()
        submit_data = {
            'userId': self.user_id,
            'answers': {}
        }
        for question in poll['questions']:
            submit_data['answers'][str(question['id'])] = f'User {self.user_id} answer'

        response = client.post(f'/api/v1/polls/{text_poll_id}', json=submit_data)
        self.assertEqual(response.status_code, 200)

    def test_duplicated_submit(self, text_poll_id):
        client = APIClient()
        response = client.get(f'/api/v1/polls/{text_poll_id}')
        self.assertEqual(response.status_code, 200)
        poll = response.json()

        submit_data = {
            'userId': self.user_id,
            'answers': {}
        }
        for question in poll['questions']:
            submit_data['answers'][str(question['id'])] = f'User {self.user_id} answer'

        response = client.get(f'/api/v1/polls/{text_poll_id}')
        self.assertEqual(response.status_code, 200)
        response = client.post(f'/api/v1/polls/{text_poll_id}', json=submit_data)
        self.assertEqual(response.status_code, 400)

    def test_submit_choice_poll(self, choice_poll_id):
        client = APIClient()
        response = client.get(f'/api/v1/polls/{choice_poll_id}')
        self.assertEqual(response.status_code, 200)
        poll = response.json()

        submit_data = {
            'userId': self.user_id,
            'answers': {}
        }
        for question in poll['questions']:
            if question['type'] == TypePoll.choice.value:
                submit_data['answers'][str(question['id'])] = 1
            elif question['type'] == TypePoll.multiple_choice.value:
                submit_data['answers'][str(question['id'])] = [1, 2]

        response = client.post(f'/api/v1/polls/{choice_poll_id}', json=submit_data)
        self.assertEqual(response.status_code, 200)

    def test_submit_text_poll_by_other_user(self, text_poll_id):
        client = APIClient()
        response = client.get(f'/api/v1/polls/{text_poll_id}')
        self.assertEqual(response.status_code, 200)
        poll = response.json()

        submit_data = {
            'userId': self.other_user_id,
            'answers': {}
        }
        for question in poll['questions']:
            submit_data['answers'][str(question['id'])] = f'User {self.other_user_id} answer'

        response = client.post(f'/api/v1/polls/{text_poll_id}', json=submit_data)
        self.assertEqual(response.status_code, 200)

    def test_polls_by_user(self, text_poll_id, choice_poll_id):
        client = APIClient()
        response = client.get(f'/api/v1/user-polls/{self.user_id}')
        self.assertEqual(response.status_code, 200)
        polls = response.json()
        """len(polls) >= 2"""
        poll_ids = [p['pollId'] for p in polls]
        self.assertIn(text_poll_id, poll_ids)
        self.assertIn(choice_poll_id, poll_ids)

    def test_polls_by_other_user(self, text_poll_id):
        client = APIClient()
        response = client.get(f'/api/v1/user-polls/{self.other_user_id}')
        self.assertEqual(response.status_code, 200)
        polls = response.json()
        """len(polls) >= 1"""
        poll_ids = [p['pollId'] for p in polls]
        self.assertIn(text_poll_id, poll_ids)
