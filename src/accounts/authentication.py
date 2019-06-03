import sys
from django.contrib.auth import get_user_model

from accounts.models import Token

User = get_user_model()


class PasswordlessAuthenticationBackend:

    def authenticate(self, uid=None):
        print('uuuuuuuuu')
        print('uid', uid, file=sys.stderr)
        if not Token.objects.filter(uid=uid).exists():
            print('no token found', file=sys.stderr)
            return None
        token = Token.objects.get(uid=uid)
        print('got token', file=sys.stderr)
        try:
            user = User.objects.get(email=token.email)
            print('got user', file=sys.stderr)
            return user
        except User.DoesNotExist:
            print('new user', file=sys.stderr)
            return User.objects.create(email=token.email)

    def get_user(self, email):
        try:
            return User.objects.get(email=email)
        except User.DoesNotExist:
            return None
