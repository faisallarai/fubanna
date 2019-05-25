from django.test import TestCase
from django.urls import reverse, resolve
from django.utils.translation import activate

from main.views import HomePageView


class HomePageViewTest(TestCase):

    def setUp(self):
        activate('en')

    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/en/')
        print('Found:', found)
        self.assertEqual(found.func.__name__, HomePageView.as_view().__name__)

    def test_uses_home_template(self):
        response = self.client.get(reverse('main:home'))
        self.assertTemplateUsed(response, 'main/home.html')

    def test_uses_base_template(self):
        response = self.client.get(reverse('main:home'))
        self.assertTemplateUsed(response, 'base.html')
