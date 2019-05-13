from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth import login, logout, REDIRECT_FIELD_NAME, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.http import is_safe_url
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic import TemplateView, FormView, RedirectView


from .forms import ContactForm, RegisterForm, LoginForm


class HomeView(TemplateView):

    template_name = 'main/home.html'

    def get_context_data(self, *args, **kwargs):
        context = super(HomeView, self).get_context_data(*args, **kwargs)
        context['title'] = 'Home Page'
        print(context)

        return context


class LoginView(FormView):

    template_name = 'auth/login.html'
    form_class = LoginForm
    success_url = reverse_lazy('main:home')
    redirect_field_name = REDIRECT_FIELD_NAME

    def get_context_data(self, *args, **kwargs):
        context = super(LoginView, self).get_context_data(*args, **kwargs)
        context['title'] = 'Login Page'
        print(context)

        return context

    @method_decorator(sensitive_post_parameters('password'))
    @method_decorator(never_cache)
    @method_decorator(csrf_protect)
    def dispatch(self, request, *args, **kwargs):
        request.session.set_test_cookie()

        return super(LoginView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        user = form.get_user()
        email = user.email
        password = user.password
        print(email)
        print(password)
        print('User LoggedIn')
        print(self.request.user.is_authenticated)
        login(self.request, user)
        print(self.request.user.is_authenticated)

        if self.request.session.test_cookie_worked():
            self.request.session.delete_test_cookie()

        return super(LoginView, self).form_valid(form)


class LogoutView(RedirectView, LoginRequiredMixin):
    url = reverse_lazy('main:home')
    permanent = False

    def get(self, request, *args, **kwargs):
        logout(request)

        return super(LogoutView, self).get(request, *args, **kwargs)


class RegisterView(FormView):

    form_class = RegisterForm
    template_name = 'auth/register.html'
    success_url = reverse_lazy('main:register')

    def get_context_data(self, *args, **kwargs):
        context = super(RegisterView, self).get_context_data(
            *args, **kwargs)
        context['title'] = 'Register Page'
        print(context)

        return context

    def form_valid(self, form):
        print(form.cleaned_data)

        return super(RegisterView, self).form_valid(form)


class ContactView(FormView):

    template_name = 'main/contact.html'
    form_class = ContactForm
    success_url = reverse_lazy('main:contact')

    def get_initial(self):
        initial = super(ContactView, self).get_initial()

        if self.request.user.is_authenticated:
            print(self.request.user)
            initial['name'] = self.request.user.get_screen_name()
            initial['email'] = self.request.user
            initial['phone_number'] = self.request.user.get_phone_number()

        return initial

    def get_context_data(self, *args, **kwargs):
        context = super(ContactView, self).get_context_data(*args, **kwargs)
        context['title'] = 'Contact Page'
        print(context)

        return context

    def form_valid(self, form):
        form.send_email()

        return super(ContactView, self).form_valid(form)
