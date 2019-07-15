import uuid

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model
from django.template.loader import render_to_string
from django.core.mail import EmailMessage

from .models import Agent, Token
from .tasks import send_register_email_task

User = get_user_model()


class LoginForm(AuthenticationForm):
    email = forms.EmailField(widget=forms.EmailInput(
        attrs={'placeholder': 'Your Email', 'class': 'keyword-input', 'id': 'login_email'}))

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


class RegisterForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.EmailInput(
        attrs={'placeholder': 'Your Email', 'class': 'keyword-input', 'id': 'register_email'}))
    phone_number = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Your Phone Number', 'class': 'keyword-input', 'id': 'phone_number'}))
    screen_name = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Your Name', 'class': 'keyword-input', 'id': 'screen_name'}))

    class Meta:
        model = Agent
        fields = ['email', 'phone_number', 'screen_name', 'slug']

    def send_email(self):
        send_register_email_task.delay(self.cleaned_data)
