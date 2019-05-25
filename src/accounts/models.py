from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class CustomUserQuerySet(models.QuerySet):
    def active(self):
        return self.filter(active=True)


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


class Token(models.Model):
    email = models.EmailField()
    uid = models.UUIDField(max_length=255)


from .tasks import send_verification_email


def user_post_save(sender, instance, signal, *args, **kwargs):
    if not instance.is_verified:
        send_verification_email.delay(instance.pk)
        print('sent')


signals.post_save.connect(user_post_save, CustomUser)
