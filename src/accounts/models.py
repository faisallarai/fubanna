import uuid
import random
import os

from django.db import models
from django.db.models.signals import pre_save
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.shortcuts import reverse

from .utils import unique_slug_generator


def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)

    return name, ext


def upload_image_path(instance, filename):
    new_filename = random.randint(1, 2343456545654)
    name, ext = get_filename_ext(filename)
    print(get_filename_ext(filename))
    final_filename = f'{new_filename}{ext}'

    return f'agents/{new_filename}/{final_filename}'


class UserManager(BaseUserManager):
    # pass
    def create_user(self, email, password=None):

        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(
            email,
            password=password,
        )
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(_('email'), primary_key=True)
    is_agent = models.BooleanField(_('agent'), default=False)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'email'
    is_anonymous = False
    is_authenticated = True

    class Meta:
        verbose_name = _('user')

    objects = UserManager()

    def __str__(self):
        return self.email

    @property
    def is_staff(self):
        return self.is_admin


class Token(models.Model):
    email = models.EmailField()
    uid = models.UUIDField(max_length=40, default=uuid.uuid4)


class Agent(models.Model):
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15)
    screen_name = models.CharField(max_length=100)
    slug = models.SlugField(blank=True, max_length=20,
                            db_index=True, unique=True)
    image = models.ImageField(
        upload_to=upload_image_path, blank=True, null=True)

    def __str__(self):
        return self.screen_name

    def get_absolute_url(self):
        return reverse('accounts:profile', args=[str(self.slug)])


# from main.tasks import send_verification_email


# def user_post_save(sender, instance, signal, *args, **kwargs):
#     if not instance.is_verified:
#         send_verification_email.delay(instance.pk)
#         print('sent')


# signals.post_save.connect(user_post_save, User)


def agent_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


pre_save.connect(agent_pre_save_receiver, sender=Agent)
