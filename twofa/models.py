from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)


class TwoFAUserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username, email, authy_id, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not username:
            raise ValueError('The given username must be set')
        email = self.normalize_email(email)
        username = self.model.normalize_username(username)
        user = self.model(username=username, email=email, authy_id=authy_id, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email=None, authy_id=None, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, email, authy_id, password, **extra_fields)

    def create_superuser(self, username, email, authy_id, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(username, email, authy_id, password, **extra_fields)


class TwoFAUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=42, unique=True)
    email = models.EmailField()
    authy_id = models.CharField(max_length=12, null=True, blank=True)

    objects = TwoFAUserManager()

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
