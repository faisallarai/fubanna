from django.test import TestCase
from django.urls import reverse
from django.utils.translation import activate
from unittest.mock import patch, call

from accounts.models import Token


class SendLoginEmailViewTest(TestCase):

    def setUp(self):
        activate('en')

    def test_redirects_to_home_page(self):
        response = self.client.post(reverse('accounts:send_login_email'), data={
            'email': 'ama@example.com'})

        self.assertRedirects(response, reverse(
            'accounts:login'), fetch_redirect_response=False)

    @patch('accounts.views.send_login_email_task.delay')
    def test_sends_mail_to_address_from_post(self, mock_send_login_email_task_delay):
        self.client.post(reverse('accounts:send_login_email'),
                         data={'email': 'ama@example.com'})

        # print(mock_send_login_email_task_delay)
        self.assertEqual(mock_send_login_email_task_delay.called, True)
        # print(mock_send_login_email_task_delay.call_args)
        self.assertEqual(
            mock_send_login_email_task_delay.call_args, call('ama@example.com'))

    def test_adds_success_message(self):
        response = self.client.post(reverse('accounts:send_login_email'), data={
            'email': 'ama@example.com'}, follow=True)
        message = list(response.context['messages'])[0]
        self.assertEqual(
            message.message, "Check your email, we've sent you a link you can use to log in.")
        self.assertEqual(message.tags, "success")

    @patch('accounts.views.messages')
    def test_adds_success_message_with_mocks(self, mock_messages):
        response = self.client.post(reverse('accounts:send_login_email'), data={
            'email': 'ama@example.com'})
        expected = "Check your email, we've sent you a link you can use to log in."
        self.assertEqual(mock_messages.success.call_args,
                         call(response.wsgi_request, expected))
