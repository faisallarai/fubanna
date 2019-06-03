from django.test import TestCase
from django.contrib.auth import get_user_model

from accounts.models import Token

User = get_user_model()


class UserModelTest(TestCase):

    def test_user_is_valid_with_email_only(self):
        user = User(email='ama@gmail.com')
        user.full_clean()  # should not raise

    def test_email_is_primary_key(self):
        user = User(email='kofi@gmail.com')
        self.assertEqual(user.pk, 'kofi@gmail.com')


class TokenModelTest(TestCase):

    def test_links_user_with_auto_generated_uid(self):
        token1 = Token.objects.create(email='ama@gmail.com')
        token2 = Token.objects.create(email='amam@gmail.com')
        self.assertNotEqual(token1.uid, token2.uid)
