from django.db import models
from django.utils import timezone
from django.contrib.auth.hashers import make_password


class TelegramUser(models.Model):
    tg_id = models.CharField(max_length=200, default='')
    login = models.CharField(max_length=200, unique=True)
    password = models.CharField(max_length=200)

    def hash_password(self, row):
        self.password = make_password(row)

    def __str__(self):
        return self.login

    def save(self, *args, **kwargs):
        self.hash_password(self.password)
        super().save(*args, **kwargs)


class Task(models.Model):
    STATUS_VARIANTS = [
        (1, None),
        (2, 'rejected'),
        (3, 'accepted'),
        (4, 'completed'),
    ]

    name = models.CharField(max_length=300)
    description = models.TextField(default='No description')
    date = models.DateField(default=timezone.now)
    user = models.ForeignKey(TelegramUser, on_delete=models.CASCADE)
    status = models.IntegerField(choices=STATUS_VARIANTS, default=1)

    def __str__(self):
        return f'{self.name} for {self.user} on {self.date}'
