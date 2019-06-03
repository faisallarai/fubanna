import uuid
import sys

from django.shortcuts import render, HttpResponseRedirect
from django.views.generic import CreateView, ListView, DetailView, TemplateView
from django.urls import reverse_lazy, reverse
from django.contrib.auth import get_user_model, login as auth_login, authenticate

from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

from accounts.forms import LoginForm, RegisterForm
from accounts.tasks import send_login_email_task

User = get_user_model()


def send_login_email(request):
    email = request.POST['email']
    send_login_email_task.delay(email)

    messages.success(
        request, "Check your email, we've sent you a link you can use to log in.")

    return HttpResponseRedirect(reverse('accounts:login'))


def activate_login_email(request, uid):
    print('uid:', uid)
    user = authenticate(uid)

    if request.user.is_authenticated:
        print('authenticated')

    if user is not None:
        print('login')
        auth_login(request, user)

    return HttpResponseRedirect(reverse('main:home'))

# def agent_activation_view(request, uidb64, token):
#     try:
#         uid = force_text(urlsafe_base64_decode(uidb64))
#         user = User.objects.get(verification_uuid=uid)
#     except (TypeError, ValueError, OverflowError, User.DoesNotExist):
#         user = None

#     if user is not None and account_activation_token.check_token(user, token):
#         user.is_active = True
#         user.is_verified = True
#         user.save()
#         login(request, user)
#         return redirect('main:home')

#     return render(request, 'main/user_activation_invalid.html')


class AgentUserListView(ListView):
    template_name = 'accounts/user_list.html'
    queryset = User.objects.all()
    context_object_name = 'users'


class AgentUserDetailView(DetailView):
    model = User
    template_name = 'main/users/user_detail.html'


class UserActivationSentView(TemplateView):
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
