from django.contrib.auth.models import BaseUserManager


class TwoFAUserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username, email, authy_id, password,
                     **extra_fields):
        if not username:
            raise ValueError('The given username must be set')
        email = self.normalize_email(email)
        username = self.model.normalize_username(username)
        user = self.model(username=username, email=email,
                          authy_id=authy_id, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email=None, authy_id=None, password=None,
                    **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(
            username,
            email,
            authy_id,
            password,
            **extra_fields
        )

    def create_superuser(self, username, email, authy_id, password,
                         **extra_fields):
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(
            username,
            email,
            authy_id,
            password,
            **extra_fields
        )
