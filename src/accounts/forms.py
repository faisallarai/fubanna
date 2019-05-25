from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model

customuser = get_user_model()


class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = customuser
        fields = ('email',)


class CustomUserChangeForm(UserChangeForm):

    class Meta(UserChangeForm):
        model = customuser
        fields = ('email',)


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Email', 'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'placeholder': 'Password', 'class': 'form-control'}))


class RegisterForm(CustomUserCreationForm):
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
        model = customuser
        fields = ('email', 'password1', 'password2',
                  'phone_number', 'screen_name')
