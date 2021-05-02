from rest_framework import serializers
from .validates import validateQuestionType
from .models import Poll, Question, OptionTheQuestion


class PollSerializer(serializers.ModelSerializer):

    class Meta:
        model = Poll
        fields = ['id', 'name', 'description', 'date_start', 'date_finish']


class CreateAdminPollSerializer(serializers.ModelSerializer):

    class Meta:
        model = Poll
        fields = ['name', 'description', 'date_start', 'date_finish']


class UpdateAdminPollSerializer(serializers.ModelSerializer):

    class Meta:
        model = Poll
        fields = ['id', 'name', 'description', 'date_finish']


class AdminQuestionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Question
        fields = ['id', 'poll', 'question_text', 'question_type']


class AdminOptionTheQuestionSerializer(serializers.ModelSerializer):

    class Meta:
        model = OptionTheQuestion
        fields = ['id', 'question', 'option_text', 'option_true']


class CompletedPollSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    created = serializers.DateTimeField(format='%Y-%m-%dT%H:%M:%S')


class QuestionSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    question_type = serializers.CharField(max_length=30, validators=[validateQuestionType])
    text = serializers.CharField(max_length=300)


class UserOptionSerializer(serializers.Serializer):
    index = serializers.IntegerField()
    text = serializers.CharField(max_length=100)
