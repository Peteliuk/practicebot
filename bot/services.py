from django.contrib.auth.hashers import make_password
from django.utils.crypto import get_random_string
from django.core.mail import send_mail

from .tasks import send_notification


class TelegramUserService:
    @staticmethod
    def create_telegram_user(obj):
        obj.password = get_random_string()
        send_mail(
            'BVBlogic practice bot',
            f'Your authorization data:\n\temail: {obj.email}\n\tpassword: {obj.password}',
            'l1999peteliuk@gmail.com',
            [f'{obj.email}'],
            fail_silently=False,
        )
        obj.password = make_password(obj.password)


class TaskService:
    @staticmethod
    def notify_bot_about_task(obj):
        if obj.user.telegram_id and obj.status == 4:
            send_notification(obj.user.telegram_id, f'<b>Task: {obj.name} {obj.get_status_display()}!</b>')
        if obj.user.telegram_id and obj.status == 1:
            send_notification(obj.user.telegram_id, f'<b>You\'ve received new task!\nName:\t</b>{obj.name}')
