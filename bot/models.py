from django.db import models
from django.utils import timezone

class TelegramUser(models.Model):
	tg_id = models.CharField(max_length=200, null=True, blank=True)
	login = models.CharField(max_length=200, unique=True)
	password = models.CharField(max_length=200)

	def __str__(self):
		return self.login


class Task(models.Model):
	name = models.CharField(max_length=300)
	description = models.TextField(default='No description')
	date = models.DateTimeField(default=timezone.now)
	user = models.ForeignKey(TelegramUser, on_delete=models.CASCADE)
	acceed = models.BooleanField(null=True, blank=True, default=None)
	complited = models.BooleanField(default=False)
	
	def __str__(self):
		return f'{self.name} for {self.user} on {self.date}'
