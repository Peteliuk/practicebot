#from django.shortcuts import render
from django.conf import settings

from rest_framework.response import Response
from rest_framework.views import APIView

from telebot import TeleBot
from telebot import types

from .models import TelegramUser

TOKEN = 'TOKEN'
bot = TeleBot(TOKEN)
 
 
class UpdateBot(APIView):
    def post(self, request):
        # Сюда должны получать сообщения от телеграм и далее обрабатываться ботом
        json_str = request.body.decode('UTF-8')
        update = types.Update.de_json(json_str)
        bot.process_new_updates([update])
 
        return Response({'code': 200})


@bot.message_handler(commands=['start'])
def start(message):
	user = TelegramUser()
	username = ''
	user_password = ''
	run = True
	chat_id = message.chat.id
	bot.send_message(chat_id, "Hello World!\n To sign up, enter your username:")
	while run:
		run = False
		if message.text != message.from_user.username:
			bot.send_message(chat_id, "Enter YOUR Telegram username!!!")
			run = True
	username = message.text
	bot.send_message(chat_id, "Great! And the last enter your new password:")
	new_password = message.text
	bot.send_message(chat_id, "Confirm password:")
	while run:
		run = False
		if message.text != new_password:
			bot.send_message(chat_id, "Password unconfirmed! Try again!")
			run = True
	user_password = new_password
	user.user_id = chat_id
	user.username = username
	user.user_password = user_password
	user.save()
	bot.send_message(chat_id, "Congratulation! You are registered! Have a nice day!")


@bot.message_handler(func=lambda message: True, content_types=['audio', 'video', 'document', 'text', 'location', 'contact', 'sticker'])
def default_command(message):
	bot.reply_to(message, "Your message")


# Webhook
#bot.set_webhook(url="http://127.0.0.1:8000/")