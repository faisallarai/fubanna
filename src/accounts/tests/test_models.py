import uuid

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils.translation import activate

from accounts.models import Agent, Token

User = get_user_model()


class UserModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        activate('en')
        User.objects.create(email='ama@example.com')

    def test_user_is_valid_with_email_only(self):
        user = User(email='ama@example.com')
        self.assertEqual(user.email, 'ama@example.com')

    def test_user_email_is_primary_key(self):
        user = User(email='kofi@gmail.com')
        self.assertEqual(user.pk, 'kofi@gmail.com')

    def test_user_email_label(self):
        user = User.objects.get(email='ama@example.com')
        label = user._meta.get_field('email').verbose_name
        self.assertEqual(label, 'email')


class TokenModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        uid = str(uuid.uuid4())
        Token.objects.create(email='ama@example.com', uid=uid)

    def test_token_email_label(self):
        token = Token.objects.get(email='ama@example.com')
        label = token._meta.get_field('email').verbose_name
        self.assertEqual(label, 'email')

    def test_token_agent_uid_label(self):
        token = Token.objects.get(email='ama@example.com')
        label = token._meta.get_field('uid').verbose_name
        self.assertEqual(label, 'uid')

    def test_token_links_user_with_auto_generated_uid(self):
        token1 = Token.objects.create(email='ama@gmail.com')
        token2 = Token.objects.create(email='kofi@gmail.com')
        self.assertNotEqual(token1.uid, token2.uid)


class AgentModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Agent.objects.create(email='ama@example.com',
                             phone_number='0243232323', screen_name='Ama Danju', slug='ama-danju')

    def test_agent_email_label(self):
        agent = Agent.objects.get(id=1)
        label = agent._meta.get_field('email').verbose_name
        self.assertEqual(label, 'email')

    def test_agent_email_is_unique(self):
        agent = Agent.objects.get(id=1)
        is_unique = agent._meta.get_field('email').unique
        self.assertTrue(is_unique)

    def test_agent_phone_number_label(self):
        agent = Agent.objects.get(id=1)
        label = agent._meta.get_field('phone_number').verbose_name
        self.assertEqual(label, 'phone number')

    def test_agent_phone_number_max_length(self):
        agent = Agent.objects.get(id=1)
        max_length = agent._meta.get_field('phone_number').max_length
        self.assertEqual(max_length, 15)

    def test_agent_screen_name_label(self):
        agent = Agent.objects.get(id=1)
        label = agent._meta.get_field('screen_name').verbose_name
        self.assertEqual(label, 'screen name')

    def test_agent_screen_name_max_length(self):
        agent = Agent.objects.get(id=1)
        max_length = agent._meta.get_field('screen_name').max_length
        self.assertEqual(max_length, 100)

    def test_agent_slug_label(self):
        agent = Agent.objects.get(id=1)
        label = agent._meta.get_field('slug').verbose_name
        self.assertEqual(label, 'slug')

    def test_agent_slug_max_length(self):
        agent = Agent.objects.get(id=1)
        max_length = agent._meta.get_field('slug').max_length
        self.assertEqual(max_length, 20)

    def test_agent_slug_db_index(self):
        agent = Agent.objects.get(id=1)
        db_index = agent._meta.get_field('slug').db_index
        self.assertTrue(db_index)

    def test_agent_slug_is_unique(self):
        agent = Agent.objects.get(id=1)
        is_unique = agent._meta.get_field('slug').unique
        self.assertTrue(is_unique)

    def test_agent_image_label(self):
        agent = Agent.objects.get(id=1)
        label = agent._meta.get_field('image').verbose_name
        self.assertEqual(label, 'image')

    def test_agent_image_is_blank(self):
        agent = Agent.objects.get(id=1)
        is_blank = agent._meta.get_field('image').blank
        self.assertTrue(is_blank)

    def test_agent_image_is_null(self):
        agent = Agent.objects.get(id=1)
        is_null = agent._meta.get_field('image').null
        self.assertTrue(is_null)

    def test_get_absolute_url(self):
        agent = Agent.objects.get(id=1)
        self.assertEqual(agent.get_absolute_url(),
                         '/en/accounts/agents/ama-danju/')

    def test_str_method(self):
        agent = Agent.objects.get(id=1)
        self.assertEqual(agent.__str__(), 'Ama Danju')
