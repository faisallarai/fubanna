import uuid

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.db.models import signals
from django.urls import reverse


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

    class Meta:
        verbose_name = _('user')

    def __str__(self):
        return self.email

    def get_screen_name(self):
        return self.screen_name

    def get_phone_number(self):
        return self.phone_number

    def get_absolute_url(self):
        return reverse('main:accounts-detail', kwargs={'pk': self.pk})


from .tasks import send_verification_email


def user_post_save(sender, instance, signal, *args, **kwargs):
    if not instance.is_verified:
        send_verification_email.delay(instance.pk)
        print('sent')


signals.post_save.connect(user_post_save, CustomUser)
