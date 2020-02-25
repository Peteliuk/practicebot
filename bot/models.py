from django.db import models
from django.utils import timezone

from bot.constants import emojis
from .managers import TaskManager
from .managers import TelegramUserManager


class TelegramUser(models.Model):
    telegram_id = models.CharField(max_length=100, default='')
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=200)

    telegram_users = TelegramUserManager()

    def __str__(self):
        return self.email


class Task(models.Model):
    STATUS_VARIANTS = [
        (1, 'created'),
        (2, f'{emojis.x} rejected'),
        (3, f'{emojis.white_check_mark} accepted'),
        (4, f'{emojis.sign_of_the_horns} completed'),
    ]

    name = models.CharField(max_length=300)
    description = models.TextField(default='No description')
    date = models.DateField(default=timezone.now)
    user = models.ForeignKey(TelegramUser, on_delete=models.CASCADE)
    status = models.IntegerField(choices=STATUS_VARIANTS, default=1)

    tasks = TaskManager()

    def __str__(self):
        return f'{self.name} for {self.user} on {self.date}'
