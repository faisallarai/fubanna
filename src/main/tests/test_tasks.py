from django.test import TestCase
from unittest.mock import patch
from unittest import mock
from django.contrib.auth import get_user_model

import main.tasks
import main.views

User = get_user_model()


class TestTasks(TestCase):

    @patch('main.tasks.send_contact_email')
    def test_task_send_contact_email(self, mock_send_contact_email):
        self.data = {
            'message': 'hello',
            'email': 'ama@gmail.com'
        }

        main.tasks.send_contact_email(data=self.data).apply()
        mock_send_contact_email.assert_called_with(data=self.data)

    @patch('main.tasks.EmailMessage.send')
    def test_can_send_contact_email(self, mock_send):
        email = main.tasks.EmailMessage(
            subject='hi', body='sweet', from_email='ama@gmail.com', to=['kofi@gmail.com'])
        email.send()
        mock_send.assert_called_once_with()

    @patch('main.tasks.EmailMessage.send', autospec=True)
    def test_can_send_contact_email_with_autospec(self, mock_send):
        email = main.tasks.EmailMessage(
            subject='hi', body='sweet', from_email='ama@gmail.com', to=['kofi@gmail.com'])
        email.send()
        mock_send.assert_called_once_with(email)
        self.assertRaises(Exception, main.tasks.EmailMessage.send)

        email2 = main.tasks.EmailMessage(
            subject='hi', body='sweet', from_email='ama@gmail.com', to=['kofi@gmail.com'])
        email2.send()
        mock_send.assert_has_calls([mock.call(email), mock.call(email2)])
