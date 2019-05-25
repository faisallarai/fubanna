import uuid
import sys

from django.shortcuts import render, redirect
from django.views.generic import CreateView, ListView, DetailView, TemplateView
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model, login
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.encoding import force_text
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_decode

from .forms import LoginForm, RegisterForm
customuser = get_user_model()


def send_subscribe_email(request):
    email = request.POST['email']
    uid = str(uuid.uuid4())
    Token.objects.create(email=email, uuid=uuid)
    url = request.build_absolute_uri(f'/accounts/subscribe?uid={uid}')
    print('saving uid', uid, 'for email', email, file=sys.stderr)
    send_mail('Your login link Fubanna',
              f'Use this link to log in: \n\n{url}', 'noreply@fubanna.com', [email])

    return render(request, 'subscribe_email_sent.html')


def activate_view(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = customuser.objects.get(verification_uuid=uid)
    except (TypeError, ValueError, OverflowError, customuser.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.is_verified = True
        user.save()
        login(request, user)
        return redirect('main:home')

    return render(request, 'main/user_activation_invalid.html')


class AgentUserListView(ListView):
    template_name = 'accounts/user_list.html'
    queryset = customuser.objects.all()
    context_object_name = 'users'


class AgentUserDetailView(DetailView):
    model = customuser
    template_name = 'main/users/user_detail.html'


class AgentActivationSentView(TemplateView):
    template_name = 'main/user_activation_sent.html'


class LoginPageView(LoginView):

    template_name = 'accounts/login.html'
    form_class = LoginForm
    success_url = reverse_lazy('main:home')

    def get_context_data(self, **kwargs):
        context = super(LoginPageView, self).get_context_data(**kwargs)
        print(context)
        return context


class LogoutPageView(LogoutView, LoginRequiredMixin):
    login_url = reverse_lazy('main:home')


class RegisterView(CreateView):

    form_class = RegisterForm
    template_name = 'auth/register.html'
    success_url = reverse_lazy('main:user_activation_sent')

    def get_context_data(self, **kwargs):
        context = super(RegisterView, self).get_context_data(**kwargs)
        context['title'] = 'Register Page'
        print(context)

        return context
