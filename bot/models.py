from django.db import models
from django.utils import timezone

class TelegramUser(models.Model):
	user_id = models.CharField(max_length=200, unique=True)
	name = models.CharField(max_length=200)
	password = models.CharField(max_length=200)
	loginned = models.BooleanField(default=False)

	def __str__(self):
		return self.name


class Task(models.Model):
	name = models.CharField(max_length=300)
	description = models.TextField()
	date = models.DateTimeField(default=timezone.now)
	user = models.ForeignKey(TelegramUser, on_delete=models.CASCADE)
	acceed = models.BooleanField(default=False)
	complited = models.BooleanField(default=False)
	
	def __str__(self):
		return f'{self.name} for {self.user} on {self.date}'