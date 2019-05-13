import uuid

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import ugettext_lazy as _
from django.db.models import signals
from django.core.mail import send_mail
from django.shortcuts import reverse
from django.conf import settings

from utils.helpers import get_image_path
from .managers import CustomUserManager


class CustomUserQuerySet(models.QuerySet):
    def active(self):
        return self.filter(active=True)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'email'

    objects = CustomUserManager()

    email = models.EmailField(_('email'), blank=False, null=False, unique=True)
    screen_name = models.CharField(
        max_length=50, blank=False, null=False, unique=True)
    is_agent = models.BooleanField(_('agent status'), default=False)
    is_staff = models.BooleanField(_('staff status'), default=False)
    is_active = models.BooleanField(_('active'), default=True)
    is_verified = models.BooleanField(_('verfied'), default=False)
    verification_uuid = models.UUIDField(
        _('unique verfication uuid'), default=uuid.uuid4)
    image = models.ImageField(
        upload_to=get_image_path, blank=False, null=False)
    phone_number = models.CharField(max_length=13, unique=True, db_index=True)

    def __str__(self):
        return self.email

    def get_screen_name(self):
        return self.screen_name

    def get_phone_number(self):
        return self.phone_number


def user_post_save(sender, instance, signal, *args, **kwargs):
    if not instance.is_verified:
        subject = 'Verify your fubanna account'
        message = 'Follow this link to verify your account: ''http://localhost:8000%s' % reverse(
            'verify', kwargs={'uuid': str(instance.verification_uuid)})
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [instance.email]
        fail_silently = False
        send_mail(subject, message, from_email, recipient_list, fail_silently)


signals.post_save.connect(user_post_save, CustomUser)
