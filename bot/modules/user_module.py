from django.db.models import Q
from bot.models import TelegramUser

class UserModule(TelegramUser):
	"""
	This is UserModule class that extends TelegramUser class.
	It provides you some functionality with `telegramuser` table in database.

	Methods:
		get_tguser_id,
		get_tguser,
		set_tguser_tg_id
	"""

	# Get telegram user's id
	def get_tguser_id(self, tg_id=None, login=None):
		"""
		:param tg_id:		user's telegram id
		:param login:		user's login in database
		return user's id from database
		"""
		
		obj = TelegramUser.objects.filter(Q(login=login) | Q(tg_id=tg_id)).first()
		return obj.id if obj else None


	# Get telegram user by id
	def get_tguser(self, id):
		"""
		Gets telegram user from database by id

		:param id:		user's id from database
		return TelegramUser object
		"""
		
		return TelegramUser.objects.get(id=id)

	# Set telegram user telegram id
	def set_tguser_tg_id(self, id, tg_id):
		"""
		Update tg_id field in database

		:param id:		id field in database
		:param tg_id:	tg_id field in database (user's telegram id)
		"""
		
		tguser = self.get_tguser(id)
		tguser.tg_id = tg_id
		tguser.save()
