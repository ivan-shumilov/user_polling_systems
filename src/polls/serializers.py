from rest_framework import serializers
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
