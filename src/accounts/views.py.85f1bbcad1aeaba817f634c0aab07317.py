
import uuid
from django.shortcuts import HttpResponseRedirect, Http404
from django.http import HttpResponseForbidden
from django.views.generic import CreateView, ListView, DetailView, TemplateView, FormView
from django.views.generic.detail import SingleObjectMixin
from django.views import View

from django.urls import reverse_lazy, reverse
from django.contrib.auth import get_user_model, login as auth_login, authenticate
from django.contrib.messages.views import SuccessMessageMixin

from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.utils.datastructures import MultiValueDictKeyError

from accounts.forms import LoginForm, RegisterForm
from accounts.tasks import send_login_email_task
from accounts.models import Agent, Token

User = get_user_model()


def send_login_email(request):
    try:
        email = request.POST['email']
    except MultiValueDictKeyError:
        email = 'faisallarai@gmail.com'

    send_login_email_task.delay(email)

    messages.success(
        request, "Check your email, we've sent you a link you can use to log in.")

    return HttpResponseRedirect(reverse('main:home'))


def activate_login_email(request, uid):
    user = authenticate(uid)

    if user is not None:
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


class AgentDisplayView(DetailView):
    model = Agent
    context_object_name = 'agent'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = RegisterForm()

        print(context)

        return context


class AgentFormView(SingleObjectMixin, FormView):
    template_name = 'accounts/profile.html'
    form_class = RegisterForm
    model = Agent

    # def get_object(self, queryset=None):

    #     slug = self.kwargs.get('slug')
    #     print("slug:", slug)

    #     try:
    #         instance = Agent.objects.get(slug=slug)
    #     except Agent.DoesNotExist:
    #         raise Http404("Not Found")
    #     except Agent.MultipleObjectsReturned:
    #         queryset = Agent.objects.filter(slug=slug)
    #         instance = queryset.first()
    #     except:
    #         raise Http404("Contact the Administartor")
    #     return instance

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()

        self.object = self.get_object()

        return super().post(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('accounts:profile', args=[str(self.object.slug)])


class AgentDetailView(View):

    def get(self, request, *args, **kwargs):
        view = AgentDisplayView.as_view()

        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = AgentFormView.as_view()

        return view(request, *args, **kwargs)


class UserActivationSentView(TemplateView):
    template_name = 'main/user_activation_sent.html'


class LoginPageView(LoginView):

    template_name = 'accounts/login.html'
    success_url = reverse_lazy('main:home')

    def get_context_data(self, **kwargs):
        context = super(LoginPageView, self).get_context_data(**kwargs)
        context['login_form'] = LoginForm()
        context['register_form'] = RegisterForm()

        return context


class LogoutPageView(LogoutView, LoginRequiredMixin):
    login_url = reverse_lazy('main:home')


class RegisterView(SuccessMessageMixin, CreateView):
    form_class = RegisterForm
    success_message = "Wait for a call from one of our Administrators."

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context

    def form_valid(self, form):
        valid = super().form_valid(form)
        uid = str(uuid.uuid4())
        email = form.cleaned_data.get('email')
        Token.objects.create(email=email, uid=uid)
        user = authenticate(uid)
        print("user:", user)
        if user is not None:
            auth_login(self.request, user)

        form.send_email()

        return valid
