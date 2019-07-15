from django.shortcuts import reverse
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys

from main.functional_tests.base import FunctionalTest


class RegistrationTest(FunctionalTest):

    def test_registration_form_submitted(self):
        '''
        Go to the home page
        Click on the login/register link
        Verify the registration form appears
        Fill in the data and submit 
        Verify the data exact was submitted
        Verify the confirmation link has been submitted to the user
        Verify link has been submitted to the administrator
        The administrator manually activate the client as an agent
        The client is sent email after the agent field is turn on
        The Client login and he sees submit property, my property
        '''

        # Go to home page
        self.browser.get(self.live_server_url + reverse('main:home'))
        with self.assertRaises(NoSuchElementException):
            self.browser.find_element_by_id('profile')

        # Locate login / register link and click it
        self.wait_for(lambda: self.browser.find_element_by_xpath(
            '//a[contains(.,"Login / Register")]').click())

        self.assertTrue(self.browser.find_element_by_id('profile'))

        self.wait_for(lambda: self.browser.find_element_by_xpath(
            '//a[contains(.,"Become an Agent")]').click())

        # Fill agent information

        email = self.browser.find_element_by_id('register_email')
        email.send_keys("faisallarai@gmail.com")
        phone_number = self.browser.find_element_by_name('phone_number')
        phone_number.send_keys("0244656852")
        screen_name = self.browser.find_element_by_name('screen_name')
        screen_name.send_keys("Issaka Faisal")

        # Locate register button and click it
        button = self.browser.find_element_by_xpath(
            '//input[@value="Register"]')
        button.click()

        # A message appears telling her an email has been sent
        self.wait_for(lambda: self.assertIn("Wait for a call from one of our Administrators.",
                                            self.browser.find_element_by_tag_name('body').text))
        # Login automatically i.e verify if logout is showing
        result = self.browser.find_element_by_xpath(
            '//a[contains(.,"Logout")]')
        self.assertTrue(result.is_displayed())

        # Go to profile page
