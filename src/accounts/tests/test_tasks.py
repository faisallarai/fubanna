from django.test import TestCase
from unittest.mock import patch
from django.contrib.auth import get_user_model
from celery.exceptions import Retry
from fubanna.celery import App
import smtplib
import uuid


import accounts.tasks
from accounts.models import Token

User = get_user_model()


class TestTasks(TestCase):

    def setUp(self):
        App.conf.update(CELERY_ALWAYS_EAGER=True)
        self.email = 'ama@example.com'
        self.uid = str(uuid.uuid4())
        Token.objects.create(email=self.email, uid=self.uid)

    @patch('accounts.tasks.EmailMessage')
    def test_send_login_email_task(self, mock_email_message):

        # call task
        token = Token.objects.get(email=self.email, uid=self.uid)
        print(token.email)
        accounts.tasks.send_login_email_task.apply_async((token.email,))
        self.assertEqual(mock_email_message.called, True)

        # patch EmailMessage
        print(mock_email_message.call_args)
        args, kwargs = mock_email_message.call_args
        subject = args[0]
        self.assertEqual(subject, 'Activate your Fubanna account.')
        self.assertEqual(kwargs, {'to': ['ama@example.com']})

    @patch('accounts.tasks.Token.objects.create')
    def test_creates_token_associated_with_email(self, mock_token):

        # call task
        token = Token.objects.get(email=self.email, uid=self.uid)
        print(token.email)
        accounts.tasks.send_login_email_task.apply_async((token.email,))
        self.assertEqual(mock_token.called, True)

        # patch EmailMessage
        args, kwargs = mock_token.call_args

        print(mock_token.call_args)
        self.assertEqual(kwargs.get('email'), 'ama@example.com')
        self.assertEqual(args, ())
