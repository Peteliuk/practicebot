from django.db import models
from django.utils import timezone

class TelegramUser(models.Model):
	user_id = models.CharField(max_length=200, unique=True)
	user_name = models.CharField(max_length=200)
	user_password = models.CharField(max_length=200)
	loginned = models.BooleanField(default=False)

	def __str__(self):
		return self.user_name


class Task(models.Model):
	task_name = models.CharField(max_length=300)
	task_description = models.TextField()
	task_date = models.DateTimeField(default=timezone.now)
	user = models.ForeignKey(TelegramUser, on_delete=models.CASCADE)
	
	def __str__(self):
		return f'{self.task_name} for {self.user} on {self.task_date}'