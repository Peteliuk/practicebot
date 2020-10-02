# Create your tasks here
from __future__ import absolute_import, unicode_literals

from celery import shared_task
from telebot import TeleBot
from .constants.strings import TOKEN

bot = TeleBot(TOKEN, threaded=False)


@shared_task
def send_notification(chat_id, text):
    bot.send_message(chat_id, text, parse_mode='HTML')


bot.set_update_listener(send_notification)
