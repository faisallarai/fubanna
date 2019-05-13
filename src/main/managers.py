from django.contrib.auth.models import BaseUserManager
from django.utils.translation import ugettext_lazy as _


class CustomUserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError(_('Email must be provided'))

        if not password:
            raise ValueError(_('Password must be provided'))

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_user(self, email=None, password=None, **extra_fields):
        return self._create_user(email, password, **extra_fields)

    def create_agentuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_agent', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_agent') is not True:
            raise ValueError(_('Agentuser must be true'))

        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must be a staff'))

        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must be true'))

        return self._create_user(email, password, **extra_fields)
