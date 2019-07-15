from selenium.webdriver.common.keys import Keys
from django.core import mail
from django.urls import reverse
from django.utils.translation import activate
import re

from main.functional_tests.base import FunctionalTest

TEST_EMAIL = 'faisal@hubtel.com'
SUBJECT = 'Your login link for Fubanna'


class LoginTest(FunctionalTest):

    def test_can_get_email_link_to_login(self):
        # Ama goes to the awesome fubanna site
        # and notices a "Log in" section in the navbar for the first time
        # It's telling her to enter her email address, so she does
        self.browser.get(self.live_server_url + reverse('accounts:login'))
        self.browser.find_element_by_id('login_email').send_keys(TEST_EMAIL)
        self.browser.find_element_by_id('login_email').send_keys(Keys.ENTER)

        # A message appears telling her an email has been sent
        self.wait_for(lambda: self.assertIn("Check your email, we've sent you a link you can use to log in.",
                                            self.browser.find_element_by_tag_name('body').text))
