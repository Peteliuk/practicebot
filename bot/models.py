from django.db import models
from django.utils import timezone
from django.contrib.auth.hashers import make_password
from django.utils.crypto import get_random_string
from django.core.mail import send_mail


class TelegramUser(models.Model):
    telegram_id = models.CharField(max_length=100, default='')
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=200)

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        self.password = get_random_string()
        send_mail(
            'BVBlogic practice bot',
            f'Your authorization data:\n\temail: {self.email}\n\tpassword: {self.password}',
            'l1999peteliuk@gmail.com',
            [f'{self.email}'],
            fail_silently=False,
        )
        self.password = make_password(self.password)
        super().save(*args, **kwargs)


class Task(models.Model):
    STATUS_VARIANTS = [
        (1, 'created'),
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
