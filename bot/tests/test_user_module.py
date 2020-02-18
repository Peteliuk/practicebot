from django.test import TestCase
from bot.modules.user_module import UserModule
from bot.models import TelegramUser


class UserModuleTestCase(TestCase):
    def setUp(self):
        self.um = UserModule()
        self.tguser = TelegramUser.objects.create(login='test', password='password')

    def test_get_tguser_id(self):
        self.assertIsInstance(self.um.get_tguser_id(login='test'), int)

    def test_get_tguser(self):
        user = self.um.get_tguser(self.um.get_tguser_id(login='test'))
        self.assertEqual(self.tguser, user)
