import sys
from django.contrib.auth import get_user_model

from accounts.models import Token

User = get_user_model()


class PasswordlessAuthenticationBackend:

    def authenticate(self, uid=None):
        if not Token.objects.filter(uid=uid).exists():
            return None
        token = Token.objects.get(uid=uid)
        try:
            user = User.objects.get(email=token.email)
            return user
        except User.DoesNotExist:
            print('new user', file=sys.stderr)
            return User.objects.create(email=token.email)

    def get_user(self, email):
        try:
            return User.objects.get(email=email)
        except User.DoesNotExist:
            return None
