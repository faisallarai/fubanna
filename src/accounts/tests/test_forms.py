from django.test import TestCase

from accounts.forms import LoginForm


class LoginFormTest(TestCase):

    def setUp(self):
        self.form = LoginForm()

    def test_form_email_input_has_placeholder(self):
        self.assertIn('placeholder="Email"', self.form.as_p())

    def test_form_email_input_has_css_classes(self):
        self.assertIn('class="keyword-input', self.form.as_p())
