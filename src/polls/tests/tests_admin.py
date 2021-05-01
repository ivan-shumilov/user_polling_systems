from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from ..models import Poll, Question, OptionTheQuestion
from users.models import User
from rest_framework.authtoken.models import Token
from ..enum import TypePoll


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


class UpdatePollTest(TestCase):

    def setUp(self):
        self.email = 'test.test@test.com'
        self.password = '123456789'
        User.objects.all().delete()
        Poll.objects.all().delete()

    def test_update_poll(self):
        client = APIClient()
        user = User.objects.create_superuser(email=self.email, password=self.password)
        token = Token.objects.create(user=user)
        client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')
        data = {'name': 'poll test1', 'description': 'description1', 'date_start': '2021-05-01 11:11',
                'date_finish': '2021-06-01 11:11'}
        poll = Poll.objects.create(**data)
        self.assertEqual(poll.name, data['name'])
        new_data = {'name': 'poll test11', 'description': 'description11', 'date_start': '2021-05-01 12:11',
                    'date_finish': '2021-06-01 12:11'}
        response = client.patch(f"{reverse('admin_polls-list')}{poll.id}/", new_data)
        self.assertEqual(response.status_code, 200)


class CreateQuestionTest(TestCase):

    def setUp(self):
        self.email = 'test.test@test.com'
        self.password = '123456789'
        User.objects.all().delete()
        Poll.objects.all().delete()
        Question.objects.all().delete()

    def test_create_question(self):
        client = APIClient()
        user = User.objects.create_superuser(email=self.email, password=self.password)
        token = Token.objects.create(user=user)
        client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')

        data = {'name': 'poll test1', 'description': 'description1', 'date_start': '2021-05-01 11:11',
                'date_finish': '2021-06-01 11:11'}
        poll = Poll.objects.create(**data)
        data_question = {'poll': poll.id, 'question_text': 'question', 'question_type': TypePoll.text.value}
        response = client.post(reverse('admin_questions-list'), data_question)
        self.assertEqual(response.status_code, 201)

    def test_wrong_create_question_incorrect_type(self):
        client = APIClient()
        user = User.objects.create_superuser(email=self.email, password=self.password)
        token = Token.objects.create(user=user)
        client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')

        data = {'name': 'poll test1', 'description': 'description1', 'date_start': '2021-05-01 11:11',
                'date_finish': '2021-06-01 11:11'}
        poll = Poll.objects.create(**data)
        data_question = {'poll': poll.id, 'question_text': 'question', 'question_type': 'incorrect_type'}
        response = client.post(reverse('admin_questions-list'), data_question)
        self.assertEqual(response.status_code, 400)

    def test_wrong_create_question(self):
        client = APIClient()
        user = User.objects.create_superuser(email=self.email, password=self.password)
        token = Token.objects.create(user=user)
        client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')

        data = {'name': 'poll test1', 'description': 'description1', 'date_start': '2021-05-01 11:11',
                'date_finish': '2021-06-01 11:11'}
        poll = Poll.objects.create(**data)
        data_question = {'poll': poll.id, 'question_type': TypePoll.text.value}
        response = client.post(reverse('admin_questions-list'), data_question)
        self.assertEqual(response.status_code, 400)

    def test_wrong_without_rulls_create_question(self):
        client = APIClient()
        user = User.objects.create_superuser(email=self.email, password=self.password)
        user.is_staff = False
        user.save()
        token = Token.objects.create(user=user)
        client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')

        data = {'name': 'poll test1', 'description': 'description1', 'date_start': '2021-05-01 11:11',
                'date_finish': '2021-06-01 11:11'}
        poll = Poll.objects.create(**data)
        data_question = {'poll': poll.id, 'question_text': 'question', 'question_type': TypePoll.text.value}
        response = client.post(reverse('admin_questions-list'), data_question)
        self.assertEqual(response.status_code, 403)


class DeleteQuestionTest(TestCase):

    def setUp(self):
        self.email = 'test.test@test.com'
        self.password = '123456789'
        User.objects.all().delete()
        Poll.objects.all().delete()
        Question.objects.all().delete()

    def test_delete_poll(self):
        client = APIClient()
        user = User.objects.create_superuser(email=self.email, password=self.password)
        token = Token.objects.create(user=user)
        client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')
        data = {'name': 'poll test1', 'description': 'description1', 'date_start': '2021-05-01 11:11',
                'date_finish': '2021-06-01 11:11'}
        poll = Poll.objects.create(**data)
        data_question = {'poll': poll, 'question_text': 'question', 'question_type': TypePoll.text.value}
        question = Question.objects.create(**data_question)
        response = client.delete(f"{reverse('admin_questions-list')}{question.id}/")
        self.assertEqual(response.status_code, 204)

    def test_wrong_delete_question_without_rulls(self):
        client = APIClient()
        user = User.objects.create_superuser(email=self.email, password=self.password)
        user.is_staff = False
        user.save()
        token = Token.objects.create(user=user)
        client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')
        data = {'name': 'poll test1', 'description': 'description1', 'date_start': '2021-05-01 11:11',
                'date_finish': '2021-06-01 11:11'}
        poll = Poll.objects.create(**data)
        data_question = {'poll': poll, 'question_text': 'question', 'question_type': TypePoll.text.value}
        question = Question.objects.create(**data_question)
        response = client.delete(f"{reverse('admin_questions-list')}{question.id}/")
        self.assertEqual(response.status_code, 403)

    def test_wrong_delete_poll_not_found(self):
        client = APIClient()
        user = User.objects.create_superuser(email=self.email, password=self.password)
        token = Token.objects.create(user=user)
        client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')
        data = {'name': 'poll test1', 'description': 'description1', 'date_start': '2021-05-01 11:11',
                'date_finish': '2021-06-01 11:11'}
        poll = Poll.objects.create(**data)
        data_question = {'poll': poll, 'question_text': 'question', 'question_type': TypePoll.text.value}
        Question.objects.create(**data_question)
        response = client.delete(f"{reverse('admin_questions-list')}999/")
        self.assertEqual(response.status_code, 404)


class UpdateQuestionTest(TestCase):

    def setUp(self):
        self.email = 'test.test@test.com'
        self.password = '123456789'
        User.objects.all().delete()
        Poll.objects.all().delete()
        Question.objects.all().delete()

    def test_update_question(self):
        client = APIClient()
        user = User.objects.create_superuser(email=self.email, password=self.password)
        token = Token.objects.create(user=user)
        client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')
        data = {'name': 'poll test1', 'description': 'description1', 'date_start': '2021-05-01 11:11',
                'date_finish': '2021-06-01 11:11'}
        poll = Poll.objects.create(**data)
        data_question = {'poll': poll, 'question_text': 'question', 'question_type': TypePoll.text.value}
        question = Question.objects.create(**data_question)
        response = client.patch(f"{reverse('admin_questions-list')}{question.id}/")
        self.assertEqual(response.status_code, 200)


class CreateOpinionTest(TestCase):

    def setUp(self):
        self.email = 'test.test@test.com'
        self.password = '123456789'
        User.objects.all().delete()
        Poll.objects.all().delete()
        Question.objects.all().delete()
        OptionTheQuestion.objects.all().delete()

    def test_create_opinion(self):
        client = APIClient()
        user = User.objects.create_superuser(email=self.email, password=self.password)
        token = Token.objects.create(user=user)
        client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')

        data = {'name': 'poll test1', 'description': 'description1', 'date_start': '2021-05-01 11:11',
                'date_finish': '2021-06-01 11:11'}
        poll = Poll.objects.create(**data)
        data_question = {'poll': poll, 'question_text': 'question', 'question_type': TypePoll.choice.value}
        question = Question.objects.create(**data_question)
        data_opinion = {'question': question.id, 'option_text': 'o1', 'option_true': True}
        response = client.post(reverse('admin_opinions-list'), data_opinion)
        self.assertEqual(response.status_code, 201)

    def test_wrong_create_opinion(self):
        client = APIClient()
        user = User.objects.create_superuser(email=self.email, password=self.password)
        token = Token.objects.create(user=user)
        client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')

        data = {'name': 'poll test1', 'description': 'description1', 'date_start': '2021-05-01 11:11',
                'date_finish': '2021-06-01 11:11'}
        poll = Poll.objects.create(**data)
        data_question = {'poll': poll, 'question_text': 'question', 'question_type': TypePoll.choice.value}
        question = Question.objects.create(**data_question)
        data_opinion = {'question': question.id, 'option_true': True}
        response = client.post(reverse('admin_opinions-list'), data_opinion)
        self.assertEqual(response.status_code, 400)

    def test_wrong_create_opinion_rulls(self):
        client = APIClient()
        user = User.objects.create_superuser(email=self.email, password=self.password)
        user.is_staff = False
        user.save()
        token = Token.objects.create(user=user)
        client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')

        data = {'name': 'poll test1', 'description': 'description1', 'date_start': '2021-05-01 11:11',
                'date_finish': '2021-06-01 11:11'}
        poll = Poll.objects.create(**data)
        data_question = {'poll': poll, 'question_text': 'question', 'question_type': TypePoll.choice.value}
        question = Question.objects.create(**data_question)
        data_opinion = {'question': question.id, 'option_text': 'o1', 'option_true': True}
        response = client.post(reverse('admin_opinions-list'), data_opinion)
        self.assertEqual(response.status_code, 403)

class DeleteOpinionTest(TestCase):

    def setUp(self):
        self.email = 'test.test@test.com'
        self.password = '123456789'
        User.objects.all().delete()
        Poll.objects.all().delete()
        Question.objects.all().delete()
        OptionTheQuestion.objects.all().delete()

    def test_delete_opinion(self):
        client = APIClient()
        user = User.objects.create_superuser(email=self.email, password=self.password)
        token = Token.objects.create(user=user)
        client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')
        data = {'name': 'poll test1', 'description': 'description1', 'date_start': '2021-05-01 11:11',
                'date_finish': '2021-06-01 11:11'}
        poll = Poll.objects.create(**data)
        data_question = {'poll': poll, 'question_text': 'question', 'question_type': TypePoll.text.value}
        question = Question.objects.create(**data_question)
        data_opinion = {'question': question, 'option_text': 'o1', 'option_true': True}
        opinion = OptionTheQuestion.objects.create(**data_opinion)
        response = client.delete(f"{reverse('admin_opinions-list')}{opinion.id}/")
        self.assertEqual(response.status_code, 204)

    def test_wrong_delete_opinion_rulls(self):
        client = APIClient()
        user = User.objects.create_superuser(email=self.email, password=self.password)
        user.is_staff = False
        user.save()
        token = Token.objects.create(user=user)
        client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')
        data = {'name': 'poll test1', 'description': 'description1', 'date_start': '2021-05-01 11:11',
                'date_finish': '2021-06-01 11:11'}
        poll = Poll.objects.create(**data)
        data_question = {'poll': poll, 'question_text': 'question', 'question_type': TypePoll.text.value}
        question = Question.objects.create(**data_question)
        data_opinion = {'question': question, 'option_text': 'o1', 'option_true': True}
        opinion = OptionTheQuestion.objects.create(**data_opinion)
        response = client.delete(f"{reverse('admin_opinions-list')}{opinion.id}/")
        self.assertEqual(response.status_code, 403)

    def test_wrong_delete_opinion_not_found(self):
        client = APIClient()
        user = User.objects.create_superuser(email=self.email, password=self.password)
        token = Token.objects.create(user=user)
        client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')
        data = {'name': 'poll test1', 'description': 'description1', 'date_start': '2021-05-01 11:11',
                'date_finish': '2021-06-01 11:11'}
        poll = Poll.objects.create(**data)
        data_question = {'poll': poll, 'question_text': 'question', 'question_type': TypePoll.text.value}
        question = Question.objects.create(**data_question)
        data_opinion = {'question': question, 'option_text': 'o1', 'option_true': True}
        OptionTheQuestion.objects.create(**data_opinion)
        response = client.delete(f"{reverse('admin_opinions-list')}1000/")
        self.assertEqual(response.status_code, 404)


class UpdateOpinionTest(TestCase):

    def setUp(self):
        self.email = 'test.test@test.com'
        self.password = '123456789'
        User.objects.all().delete()
        Poll.objects.all().delete()
        Question.objects.all().delete()
        OptionTheQuestion.objects.all().delete()

    def test_update_opinion(self):
        client = APIClient()
        user = User.objects.create_superuser(email=self.email, password=self.password)
        token = Token.objects.create(user=user)
        client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')
        data = {'name': 'poll test1', 'description': 'description1', 'date_start': '2021-05-01 11:11',
                'date_finish': '2021-06-01 11:11'}
        poll = Poll.objects.create(**data)
        data_question = {'poll': poll, 'question_text': 'question', 'question_type': TypePoll.text.value}
        question = Question.objects.create(**data_question)
        data_opinion = {'question': question, 'option_text': 'o1', 'option_true': True}
        opinion = OptionTheQuestion.objects.create(**data_opinion)
        response = client.patch(f"{reverse('admin_opinions-list')}{opinion.id}/")
        self.assertEqual(response.status_code, 200)
