import json
from rest_framework import views
from datetime import date
from rest_framework.response import Response
from rest_framework.exceptions import ParseError
from django.http import Http404
from ..models import Poll, CompletedPoll, UserAnswer, Question, OptionTheQuestion
from ..serializers import PollSerializer, CompletedPollSerializer, QuestionSerializer, UserOptionSerializer
from ..enum import TypePoll


class PollsAPIView(views.APIView):
    permission_classes = []

    def get(self, request):
        today = date.today()
        return Response(PollSerializer(Poll.objects.filter(date_start__lte=today, date_finish__gt=today),
                                       many=True).data)


class UserPolls(views.APIView):
    permission_classes = []

    def get(self, request, id):
        try:
            result = []
            for completed_poll in CompletedPoll.objects.filter(user_id=id).order_by('created'):
                completedPollDict = CompletedPollSerializer(completed_poll).data
                completedPollDict['poll_id'] = completed_poll.poll_id
                completedPollDict['answers'] = []
                for answer in UserAnswer.objects.filter(completed_poll=completed_poll):
                    answer_text = answer.answer
                    if answer.question.question_type == TypePoll.multiple_choice.value:
                        answer_text = json.loads(answer_text)
                    completedPollDict['answers'].append({
                        'question': {
                            'id': answer.question.id,
                            'type': answer.question.question_type,
                            'text': answer.answer
                        },
                        'answer': answer_text
                    })
                result.append(completedPollDict)
            return Response(result)
        except Exception as ex:
            raise ParseError(ex)


class IdPoll(views.APIView):
    def get(self, request, id):
        try:
            today = date.today()
            poll = Poll.objects.get(id=id)
            if poll.date_start > today or poll.date_finish < today:
                raise Poll.DoesNotExist()

            result = PollSerializer(poll).data
            result['questions'] = []
            for question in Question.objects.filter(poll=poll):
                questionDict = QuestionSerializer(question).data
                if question.hasOptionType:
                    questionDict['options'] = UserOptionSerializer(OptionTheQuestion.objects.filter(question=question),
                                                                   many=True).data
                result['questions'].append(questionDict)

            return Response(result)

        except Poll.DoesNotExist:
            raise Http404()
        except Exception as ex:
            raise ParseError(ex)
