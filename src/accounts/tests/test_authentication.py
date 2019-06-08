from django.test import TestCase
from django.contrib.auth import get_user_model, authenticate

from accounts.models import Token

User = get_user_model()


class AuthenticationTest(TestCase):

    def test_returns_None_if_no_such_token(self):
        result = authenticate(
            '2bbec969-e289-4b1f-a080-d8de58045094')
        self.assertIsNone(result)

    def test_returns_new_user_with_correct_email_if_token_exists(self):
        email = 'ama@gmail.com'
        token = Token.objects.create(email=email)
        user = authenticate(token.uid)
        new_user = User.objects.get(email=email)
        self.assertEqual(user, new_user)

    def test_returns_existing_user_with_correct_email_if_token_exists(self):
        email = 'ama@gmail.com'
        existing_user = User.objects.create(email=email)
        token = Token.objects.create(email=email)
        user = authenticate(token.uid)
        self.assertEqual(user, existing_user)
