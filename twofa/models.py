from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

from .managers import TwoFAUserManager


class TwoFAUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=42, unique=True)
    email = models.EmailField()
    authy_id = models.CharField(max_length=12, null=True, blank=True)

    objects = TwoFAUserManager()

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
