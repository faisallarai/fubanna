from selenium.webdriver.common.keys import Keys
from django.core import mail
from django.urls import reverse
from django.utils.translation import activate
import re

from main.functional_tests.base import FunctionalTest

TEST_EMAIL = 'ama@gmail.com'
SUBJECT = 'Your login link for Fubanna'


class LoginTest(FunctionalTest):

    def test_can_get_email_link_to_login(self):
        # Ama goes to the awesome fubanna site
        # and notices a "Log in" section in the navbar for the first time
        # It's telling her to enter her email address, so she does
        self.browser.get(self.live_server_url + reverse('accounts:login'))
        self.browser.find_element_by_name('email').send_keys(TEST_EMAIL)
        self.browser.find_element_by_name('email').send_keys(Keys.ENTER)

        # A message appears telling her an email has been sent
        self.wait_for(lambda: self.assertIn("Check your email, we've sent you a link you can use to log in.",
                                            self.browser.find_element_by_tag_name('body')))

        # She checks her email and finds a message
        email = mail.outbox[0]
        self.assertIn(TEST_EMAIL, email.to)
        self.assertEqual(email.subject, SUBJECT)

        # It has a url link in it
        self.assertIn('Use this link to log in', email.body)
        url_search = re.search(r'http://.+/.+$', email.body)
        if not url_search:
            self.fail(f'Could not find url in email body:\n{email.body}')

        url = url_search.group(0)
        self.assertIn(self.live_server_url, url)

        # She clicks it
        self.browser.get(url)

        # She is logged in
        self.wait_for(
            lambda: self.browser.find_element_by_link_text('Log out'))
        navbar = self.browser.find_element_by_css_selector('.navbar')
        self.assertIn(TEST_EMAIL, navbar.text)
