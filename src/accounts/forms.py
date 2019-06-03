from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import get_user_model
from django.template.loader import render_to_string
from django.core.mail import EmailMessage

from .models import Token

User = get_user_model()


class LoginForm(AuthenticationForm):
    email = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Email', 'class': 'keyword-input', 'name': 'email'}))

    def send_email(self):
        # later put it in task
        # send_login_email.delay(self.cleaned_data)

        email = self.cleaned_data.get('email')
        token = Token.objects.get(email=email)
        current_site = 'localhost:8000'
        mail_subject = 'Activate your Fubanna account.'
        message = render_to_string('accounts/login_activation_email.html', {
            'domain': current_site,
            'uid': token.uid
        })
        email = EmailMessage(
            mail_subject, message, to=[email]
        )
        email.send()


class RegisterForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(
        attrs={'placeholder': 'Email Address'}))
    password1 = forms.CharField(widget=forms.PasswordInput(
        attrs={'placeholder': 'Password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={'placeholder': 'Confirm Password'}))
    phone_number = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Your Phone Number'}))
    screen_name = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Your Name'}))

    class Meta(UserCreationForm):
        model = User
        fields = ('email', 'password1', 'password2',
                  'phone_number', 'screen_name')
