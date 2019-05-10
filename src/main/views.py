from django.shortcuts import render
from django.views.generic import TemplateView


class HomePageView(TemplateView):

    template_name = 'home.html'

    def get_context_data(self, *args, **kwargs):
        context = super(HomePageView, self).get_context_data(*args, **kwargs)
        context['title'] = 'Home Page'
        print(context)

        return context


class LoginPageView(TemplateView):

    template_name = 'login.html'

    def get_context_data(self, *args, **kwargs):
        context = super(LoginPageView, self).get_context_data(*args, **kwargs)
        context['title'] = 'Login Page'
        print(context)

        return context


class RegisterPageView(TemplateView):

    template_name = 'register.html'

    def get_context_data(self, *args, **kwargs):
        context = super(RegisterPageView, self).get_context_data(
            *args, **kwargs)
        context['title'] = 'Register Page'
        print(context)

        return context
