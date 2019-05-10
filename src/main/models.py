from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    is_agent = models.BooleanField(default=False, verbose_name='agent status')
    is_client = models.BooleanField(default=True, verbose_name='client status')

    def __str__(self):
        return self.email


class Agent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    other_name = models.CharField(max_length=25)
    image = models.ImageField(
        upload_to=get_image_path, blank=False, null=False)
    mobile_number = models.CharField(max_length=13)

    def __str__(self):
        return f'{self.last_name} | {self.first_name} | {self.other_name}'
