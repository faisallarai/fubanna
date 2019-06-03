from datetime import date

from selenium import webdriver
from django.urls import reverse
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.utils.translation import activate
from django.utils.translation import ugettext_lazy as _
from django.utils import formats


class HomeNewVisitorTest(StaticLiveServerTestCase):

    # It is run for every test method
    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)
        activate('en')

    def tearDown(self):
        self.browser.quit()

    def get_full_url(self, namespace):
        return self.live_server_url + reverse(namespace)

    def test_home_title(self):
        self.browser.get(self.get_full_url('main:home'))
        self.assertIn('Fubanna', self.browser.title)

    def test_home_files(self):
        self.browser.get(self.live_server_url + '/robots.txt')
        self.assertNotIn('not found', self.browser.title)
        self.browser.get(self.live_server_url + '/humans.txt')
        self.assertNotIn('not found', self.browser.title)

    def test_internalization(self):
        for lang, a_text in [('en', 'view Properties'), ('fr', 'view ee')]:
            activate(lang)

            self.browser.get(self.get_full_url('main:home'))
            a = self.browser.find_element_by_id('properties')
            self.assertEqual(_(a.get_property('text')), a_text)

    def test_localization(self):
        today = date.today()
        for lang in ['en', 'fr']:
            activate(lang)
            self.browser.get(self.get_full_url("main:home"))
            local_date = self.browser.find_element_by_id('local-date')
            self.assertEqual(formats.date_format(today, use_l10n=True),
                             local_date.text)

    def test_timezone(self):
        self.browser.get(self.get_full_url('main:home'))
        tz = self.browser.find_element_by_id('time-tz').text
        utc = self.browser.find_element_by_id('time-utc').text
        ny = self.browser.find_element_by_id('time-ny').text
        # self.assertNotEqual(tz, utc)  # Africa/Accra is the same
        self.assertNotIn(ny, [tz, utc])
