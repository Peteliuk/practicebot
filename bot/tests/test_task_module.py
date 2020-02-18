from django.test import TestCase
from bot.modules.task_module import TaskModule
from bot.models import Task
from bot.models import TelegramUser


class TaskModuleTestCase(TestCase):
    def setUp(self):
        self.tm = TaskModule()
        self.tguser = TelegramUser.objects.create(login='test', password='password')
        Task.objects.create(name='Future task', date='2020-02-19', user=self.tguser)
        Task.objects.create(name='Present task', date='2020-02-18', user=self.tguser)
        Task.objects.create(name='Past task', date='2020-02-17', user=self.tguser)

    def test_get_all_tasks(self):
        self.assertIsInstance(self.tm.get_all_tasks(self.tguser.id), object)

    def test_get_future_tasks(self):
        self.assertIsInstance(self.tm.get_future_tasks(self.tguser.id), object)

    def test_get_past_tasks(self):
        self.assertIsInstance(self.tm.get_past_tasks(self.tguser.id), object)

    def test_get_task(self):
        self.assertIsInstance(self.tm.get_task(self.tguser.task_set.first().id), object)
