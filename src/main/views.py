
import datetime

from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.translation import ugettext_lazy as _
from django.views.generic import TemplateView, FormView

from .forms import ContactForm


def home_files(request, filename):
    return render(request, filename, {}, content_type='text/plain')


class HomePageView(TemplateView):

    template_name = 'main/home.html'
    today = datetime.date.today()

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        context['title'] = _('Home Page')
        context['today'] = self.today
        print(context)

        return context


class ContactPageView(FormView):

    template_name = 'main/contact.html'
    form_class = ContactForm
    success_url = reverse_lazy('main:contact')

    def get_initial(self):
        initial = super().get_initial()

        if self.request.user.is_authenticated:
            initial['name'] = self.request.user.get_screen_name()
            initial['email'] = self.request.user
            initial['phone_number'] = self.request.user.get_phone_number()

        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Contact Page'

        return context

    def form_valid(self, form):
        form.send_email()

        return super().form_valid(form)
