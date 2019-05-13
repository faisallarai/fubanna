from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from django.core.mail import send_mail
from django.conf import settings

from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('email',)


class CustomUserChangeForm(UserChangeForm):

    class Meta(UserChangeForm):
        model = CustomUser
        fields = ('email',)


class LoginForm(AuthenticationForm):
    def confirm_login_allowed(self, user):
        pass


class RegisterForm(CustomUserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(
        attrs={'placeholder': 'Email Address'}))
    password1 = forms.CharField(widget=forms.PasswordInput(
        attrs={'placeholder': 'Password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={'placeholder': 'Confirm Password'}))

    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('email', 'password1', 'password2')


class ContactForm(forms.Form):
    name = forms.CharField(max_length=50, widget=forms.TextInput(
        attrs={'palceholder': 'Your name'}))
    phone_number = forms.CharField(max_length=15, widget=forms.TextInput(
        attrs={"placeholder": 'Phone Number'}))
    email = forms.EmailField(widget=forms.EmailInput(
        attrs={"placeholder": 'Email Address'}))
    message = forms.CharField(widget=forms.Textarea(
        attrs={"placeholder": 'Message'}))

    def send_email(self):

        subject = 'Contact Us'
        message = self.cleaned_data.get('message')
        from_email = self.cleaned_data.get('email')
        recipient_list = [settings.EMAIL_HOST_USER]
        fail_silently = False
        send_mail(subject, message, from_email, recipient_list, fail_silently)
