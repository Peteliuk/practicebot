from django.db.models import Q
from bot.models import TelegramUser


class UserModule:
    """
    This is UserModule class that
    provides you some functionality with `telegramuser` table in database.

    Methods:
        get_telegram_user,
        set_telegram_user_telegram_id
    """

    def get_telegram_user(self, user_id=None, email=None, telegram_id=None):
        """
        Return telegram user object from database by id, or email, or telegram_id

        :param user_id:		    user's id in database
        :param email:           user's email in database
        :param telegram_id:     user's telegram id in database
        """

        return TelegramUser.objects.filter(Q(id=user_id) | Q(email=email) | Q(telegram_id=telegram_id)).first()

    def set_telegram_user_telegram_id(self, user_id, telegram_id):
        """
        Update `telegram id` field in database for some user

        :param user_id:         user's id in database
        :param telegram_id:     user's telegram id in database
        """
        TelegramUser.objects.filter(id=user_id).update(telegram_id=telegram_id)
