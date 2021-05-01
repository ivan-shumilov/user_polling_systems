from django.utils.translation import ugettext as _
from rest_framework import serializers
from django.contrib.auth import login, authenticate
from rest_framework.exceptions import ValidationError
from .models import User


class SignInSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def get_authenticated_user(self, request):
        user = authenticate(request, **self.validated_data)
        if user is not None:
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return user
        raise ValidationError(_('failed authorization'))

    def validate_email(self, value):
        try:
            User.objects.get(email=value)
        except User.DoesNotExist:
            raise ValidationError(_('there is no user with this email address'))
        return value


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'email']
