from rest_framework import serializers
from .models import Poll


class AdminPollSerializer(serializers.ModelSerializer):

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
