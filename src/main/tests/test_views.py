
from django.test import TestCase
from django.urls import reverse, resolve
from django.utils.translation import activate
from django.core import mail
from unittest.mock import patch

from main.views import HomePageView, ContactPageView
from main.forms import ContactForm

import main.views


class HomePageViewTest(TestCase):

    def setUp(self):
        activate('en')

    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/en/')
        self.assertEqual(found.func.__name__, HomePageView.as_view().__name__)

    def test_uses_home_template(self):
        response = self.client.get(reverse('main:home'))
        self.assertTemplateUsed(response, 'main/home.html')

    def test_uses_base_template(self):
        response = self.client.get(reverse('main:home'))
        self.assertTemplateUsed(response, 'base.html')


class ContactPageViewTest(TestCase):

    def setUp(self):
        activate('en')
        self.form = {
            'name': 'Ama',
            'phone_number': '0243454545',
            'message': 'hi',
            'email': 'ama@gmail.com'
        }

    def test_contact_form_is_valid(self):

        form = ContactForm(data=self.form)
        self.assertTrue(form.is_valid())
