import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fubanna.settings')

App = Celery('fubanna')
App.config_from_object('django.conf:settings', namespace='CELERY')
App.autodiscover_tasks()


@App.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
