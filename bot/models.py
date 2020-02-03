from django.db import models


class TelegramUser(models.Model):
	user_id = models.CharField(max_length=200)
	username = models.CharField(max_length=200)
	user_password = models.CharField(max_length=200)

	def __str__(self):
		return f'{self.user_id}, {self.username}'
