from django.test import TestCase
from django.contrib.auth import get_user_model

CUSTOMUSER = get_user_model()


class UserManagerTest(TestCase):

    # Run once
    @classmethod
    def setUpTestData(cls):
        CUSTOMUSER.objects.create_user(
            email='user@gmail.com', password='user', phone_number='0244656851', screen_name='user')
        CUSTOMUSER.objects.create_superuser(
            email='superuser@gmail.com', password='superuser', phone_number='0244656853', screen_name='superuser')
        CUSTOMUSER.objects.create_agentuser(
            email='agentuser@gmail.com', password='agentuser', phone_number='0244656854', screen_name='agentuser')

    def test_create_user(self):
        user = CUSTOMUSER.objects.get(id=1)

        self.assertEqual(user.email, 'user@gmail.com')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

        try:
            self.assertIsNone(user.username)
        except AttributeError:
            pass

        with self.assertRaises(ValueError):
            CUSTOMUSER.objects.create_user(email='', password='user')

    def test_create_superuser(self):

        user = CUSTOMUSER.objects.get(id=2)
        self.assertEqual(user.email, 'superuser@gmail.com')
        self.assertTrue(user.is_active)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)

        try:
            self.assertIsNone(user.username)
        except AttributeError:
            pass

        with self.assertRaises(ValueError):
            CUSTOMUSER.objects.create_superuser(
                email='superusertest@gmail.com', password='superusertest', is_superuser=False, phone_number='0244656856', screen_name='superusertest')

    def test_create_agentuser(self):
        user = CUSTOMUSER.objects.get(id=3)
        self.assertEqual(user.email, 'agentuser@gmail.com')
        self.assertTrue(user.is_agent)
        self.assertTrue(user.is_active)

        try:
            self.assertIsNone(user.username)
        except AttributeError:
            pass

        with self.assertRaises(ValueError):
            CUSTOMUSER.objects.create_agentuser(email='', password='')

        with self.assertRaises(ValueError):
            CUSTOMUSER.objects.create_agentuser(
                email='agentusertest@gmail.com', password='usertest', is_agent=False, phone_number='0244656857', screen_name='agentusertest')
