from django.test import TestCase

from django.utils import timezone

from bot.models import TelegramUser
from bot.models import Task

from bot.constants.variables import STATUS_VARIANTS


class TelegramUserModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        TelegramUser.objects.create(email='example@mail.ru')

    def setUp(self):
        self.user = TelegramUser.objects.get(id=1)

    def test_telegram_id_max_length(self):
        max_length = self.user._meta.get_field('telegram_id').max_length
        self.assertEqual(max_length, 100)

    def test_telegram_id_is_nullable(self):
        nullable = self.user._meta.get_field('telegram_id').null
        self.assertTrue(nullable)

    def test_email_is_unique(self):
        unique = self.user._meta.get_field('email').unique
        self.assertTrue(unique)

    def test_password_max_length(self):
        max_length = self.user._meta.get_field('password').max_length
        self.assertEqual(max_length, 200)

    def test_object_name_equals_email(self):
        object_name = self.user.email
        self.assertEqual(object_name, str(self.user))


class TaskModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = TelegramUser.objects.create(email='example@mail.ru')
        Task.objects.create(name='Test Task', user=user)

    def setUp(self):
        self.task = Task.objects.get(id=1)

    def test_name_max_length(self):
        max_length = self.task._meta.get_field('name').max_length
        self.assertEqual(max_length, 100)

    def test_description_default_value(self):
        default = self.task._meta.get_field('description').default
        self.assertEqual(default, 'No description')

    def test_date_default_value(self):
        default = self.task._meta.get_field('date').default
        self.assertEqual(default(), timezone.now())

    def test_user_instance(self):
        self.assertIsInstance(self.task.user, TelegramUser)

    def test_status_choices(self):
        choices = self.task._meta.get_field('status').choices
        self.assertEqual(choices, STATUS_VARIANTS)

    def test_status_default(self):
        default = self.task._meta.get_field('status').default
        self.assertEqual(default, 1)
