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

    @staticmethod
    def get_telegram_user(user_id=None, email=None, telegram_id=None):
        """
        Return telegram user object by id, or email, or telegram_id fields from database

        :param user_id:		    user's id in database
        :param email:           user's email in database
        :param telegram_id:     user's telegram id in database
        """

        return TelegramUser.telegram_users.get_telegram_user(Q(id=user_id) | Q(email=email) | Q(telegram_id=telegram_id))

    @staticmethod
    def set_telegram_user_telegram_id(user_id, telegram_id):
        """
        Update `telegram id` field in database for some user

        :param user_id:         user's id in database
        :param telegram_id:     user's telegram id in database
        """
        TelegramUser.telegram_users.set_telegram_user_telegram_id(user_id, telegram_id)
