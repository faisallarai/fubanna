from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils.translation import activate


class CustomUserModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model()
        cls.user.objects.create_user(
            email='user@gmail.com', password='user', phone_number='0244454323', screen_name='usertest')

        activate('en')

    def test_email_label(self):
        user = self.user.objects.get(id=1)
        field_label = user._meta.get_field('email').verbose_name
        self.assertEqual(field_label, 'email')

    def test_phone_number_label(self):
        user = self.user.objects.get(id=1)
        field_label = user._meta.get_field('phone_number').verbose_name
        self.assertEqual(field_label, 'phone number')

    def test_screen_name_label(self):
        user = self.user.objects.get(id=1)
        field_label = user._meta.get_field('screen_name').verbose_name
        self.assertEqual(field_label, 'screen name')

    def test_phone_number_max_length(self):
        user = self.user.objects.get(id=1)
        max_length = user._meta.get_field('phone_number').max_length
        self.assertEqual(max_length, 13)

    def test_screen_name_max_length(self):
        user = self.user.objects.get(id=1)
        max_length = user._meta.get_field('screen_name').max_length
        self.assertEqual(max_length, 50)

    def test_get_absolute_url(self):
        for lang in ['en', 'fr']:
            activate(lang)
            user = self.user.objects.get(id=1)
            url = user.get_absolute_url()
            self.assertEqual(url, '/' + lang + '/accounts/1/')
