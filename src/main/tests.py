from django.test import TestCase
from django.contrib.auth import get_user_model

User = get_user_model()


class UserManagerTest(TestCase):

    def test_create_user(self):
        user = User.objects.create_user(
            email='user@gmail.com', password='user')
        self.assertEqual(user.email, 'user@gmail.com')
        self.assertEqual(user.password, 'user')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

        try:
            self.assertIsNone(user.username)
        except AttributeError:
            pass

        with self.assertRaises(TypeError):
            User.objects.create_user()

        with self.assertRaises(TypeError):
            User.objects.create_user(email='')

        with self.assertRaises(ValueError):
            User.objects.create_user(emai='', password='user')

    def test_create_superuser(self):

        user = User.objects.create_superuser(
            email='superuser@gmail.com', password='superuser')
        self.assertEqual(user.email, 'superuser@gmail.com')
        self.assertEqual(user.password, 'superuser')
        self.assertTrue(user.is_active)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)

        try:
            self.assertIsNone(user.username)
        except AttributeError:
            pass

        with self.assertRaises(TypeError):
            User.objects.create_superuser()

        with self.assertRaises(TypeError):
            User.objects.create_superuser(email='')

        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                email='superuser@gmail.com', password='superuser', is_superuser=False)

    def test_create_agentuser(self):
        user = User.objects.create(email='user@gmail.com', password='user')
        self.assertEqual(user.email, 'user@gmail.com')
        self.assertEqual(user.password, 'user')
        self.assertTrue(user.is_agent)
        self.assertTrue(user.is_active)

        try:
            self.assertIsNone(user.username)
        except AttributeError:
            pass

        with self.assertRaises(TypeError):
            User.objects.create_agentuser()

        with self.assertRaises(TypeError):
            User.objects.create_agentuser(email='')

        with self.assertRaises(ValueError):
            User.objects.create_agentuser(email='', password='')

        with self.assertRaises(ValueError):
            User.objects.create_agentuser(
                email='user@gmail.com', password='user', is_agent=False)
