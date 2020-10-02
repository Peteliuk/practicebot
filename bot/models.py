from django.db import models
from django.utils import timezone

from .managers import TaskManager
from .managers import TelegramUserManager

from .constants.variables import STATUS_VARIANTS


class TelegramUser(models.Model):
    telegram_id = models.CharField(max_length=100, null=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=200)

    objects = TelegramUserManager()

    def __str__(self):
        return self.email


class Task(models.Model):
    name = models.CharField(max_length=300)
    description = models.TextField(default='No description')
    date = models.DateField(default=timezone.now)
    user = models.ForeignKey(TelegramUser, on_delete=models.CASCADE)
    status = models.IntegerField(choices=STATUS_VARIANTS, default=1)

    objects = TaskManager()

    def __str__(self):
        return f'{self.name} for {self.user} on {self.date}'
