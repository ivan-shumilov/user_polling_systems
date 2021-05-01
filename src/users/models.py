from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):

    def _create_user(self, email, password,
                     is_staff, is_superuser, **extra_fields):
        now = timezone.now()
        email = self.normalize_email(email)
        user = self.model(email=email,
                          is_staff=is_staff, is_active=True,
                          is_superuser=is_superuser, last_login=now,
                          date_joined=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        return self._create_user(email, password, False, False,
                                 **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        return self._create_user(email, password, True, True, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    name = models.EmailField(verbose_name=_('name'))
    email = models.EmailField(verbose_name=_('email'), unique=True)
    phone = models.CharField(verbose_name=_('phone'), max_length=256, null=True, blank=True)

    register_token = models.CharField(verbose_name=_('register token'), max_length=32, null=True, blank=True)
    password_reset_token = models.CharField(verbose_name=_('password reset token'), max_length=32, null=True,
                                            blank=True)
    is_staff = models.BooleanField(verbose_name=_('is staff'), default=False)
    is_active = models.BooleanField(verbose_name=_('is active'), default=True, help_text=_('is active help'))
    date_joined = models.DateTimeField(verbose_name=_('date joined'), default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        app_label = 'users'

    def __str__(self):
        return self.email
