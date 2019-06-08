import uuid

from django.db import models
from django.db.models import signals
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin


class UserManager(BaseUserManager):

    def create_user(self, email, password=None):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(email=self.normalize_email(email))

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):

        user = self.create_user(
            email=email,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(_('email'), primary_key=True)
    is_agent = models.BooleanField(_('agent'), default=False)
    is_admin = models.BooleanField(_('staff'), default=False)

    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'email'
    is_anonymous = False
    is_authenticated = True

    class Meta:
        verbose_name = _('user')

    objects = UserManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        return self.is_admin

    @property
    def is_active(self):
        return True


class Token(models.Model):
    email = models.EmailField()
    uid = models.UUIDField(max_length=40, default=uuid.uuid4)


# from main.tasks import send_verification_email


# def user_post_save(sender, instance, signal, *args, **kwargs):
#     if not instance.is_verified:
#         send_verification_email.delay(instance.pk)
#         print('sent')


# signals.post_save.connect(user_post_save, User)
