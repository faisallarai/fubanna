import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fubanna.settings')

APP = Celery('fubanna')
APP.config_from_object('django.conf:settings')
APP.autodiscover_tasks()
