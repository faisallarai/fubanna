
import datetime

from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth import login, get_user_model
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _
from django.views.generic import TemplateView, FormView, CreateView, ListView, DetailView


from utils.tokens import account_activation_token
from .forms import ContactForm, RegisterForm, LoginForm


CUSTOMUSER = get_user_model()


def home_files(request, filename):
    return render(request, filename, {}, content_type='text/plain')


class HomePageView(TemplateView):

    template_name = 'main/home.html'
    today = datetime.date.today()

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        context['title'] = _('Home Page')
        context['today'] = self.today
        context['now'] = now()
        print(context)

        return context


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

    def get_context_data(self, **kwargs):
        context = super(ContactView, self).get_context_data(**kwargs)
        context['title'] = 'Contact Page'
        print(context)

        return context

    def form_valid(self, form):
        form.send_email()

        return super(ContactView, self).form_valid(form)
