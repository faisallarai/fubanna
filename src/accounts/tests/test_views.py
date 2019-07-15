from django.test import TestCase
from django.urls import reverse
from django.utils.translation import activate
from unittest.mock import patch, call

from accounts.models import Agent


class LoginViewTest(TestCase):

    def setUp(self):
        activate('en')

    def test_redirects_to_home_page(self):
        response = self.client.post(reverse('accounts:send_login_email'), data={
            'email': 'ama@example.com'})

        self.assertRedirects(response, reverse(
            'main:home'), fetch_redirect_response=False)

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


class AgentDetailViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Agent.objects.create(email='ama@example.com', phone_number='0243454545',
                             screen_name='Ama Danju', slug='ama-danju')

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/en/accounts/agents/ama-danju/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        agent = Agent.objects.get(id=1)
        response = self.client.get(
            reverse('accounts:profile', args=[str(agent.slug)]))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        agent = Agent.objects.get(email='ama@example.com')
        response = self.client.get(
            reverse('accounts:profile', args=[str(agent.slug)]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/profile.html')
