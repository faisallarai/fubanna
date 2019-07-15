from django.test import TestCase

from accounts.forms import LoginForm, RegisterForm


class LoginFormTest(TestCase):

    def setUp(self):
        self.form = LoginForm()

    def test_form_email_input_has_placeholder(self):
        self.assertIn('placeholder="Your Email"', self.form.as_p())

    def test_form_email_input_has_css_classes(self):
        self.assertIn('class="keyword-input"', self.form.as_p())

    def test_form_email_input_has_id(self):
        self.assertIn('id="login_email"', self.form.as_p())

    def test_form_email_input_label(self):
        self.assertTrue(
            self.form.fields['email'].label is None or self.form.fields['email'].label == 'email')


class RegisterFormTest(TestCase):

    def setUp(self):
        self.form = RegisterForm()

    def test_register_form_email_input_has_placeholder(self):
        self.assertIn('placeholder="Your Email"', self.form.as_p())

    def test_register_form_email_input_has_css_classes(self):
        self.assertIn('class="keyword-input"', self.form.as_p())

    def test_register_form_email_input_has_id(self):
        self.assertIn('id="register_email"', self.form.as_p())

    def test_register_form_email_input_label(self):
        self.assertTrue(
            self.form.fields['email'].label is None or self.form.fields['email'].label == 'email')

    def test_register_form_phone_number_input_has_placeholder(self):
        self.assertIn('placeholder="Your Phone Number"', self.form.as_p())

    def test_register_form_phone_number_input_has_css_classes(self):
        self.assertIn('class="keyword-input"', self.form.as_p())

    def test_register_form_phone_number_input_has_id(self):
        self.assertIn('id="phone_number"', self.form.as_p())

    def test_register_form_phone_number_input_label(self):
        self.assertTrue(
            self.form.fields['phone_number'].label is None or self.form.fields['phone_number'].label == 'phone number')

    def test_register_form_screen_name_input_has_placeholder(self):
        self.assertIn('placeholder="Your Name"', self.form.as_p())

    def test_register_form_screen_name_input_has_css_classes(self):
        self.assertIn('class="keyword-input"', self.form.as_p())

    def test_register_form_screen_name_input_has_id(self):
        self.assertIn('id="screen_name"', self.form.as_p())

    def test_register_form_screen_name_input_label(self):
        self.assertTrue(
            self.form.fields['screen_name'].label is None or self.form.fields['screen_name'].label == 'screen_name')
