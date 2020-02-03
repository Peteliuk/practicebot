#from django.shortcuts import render
from django.conf import settings

from rest_framework.response import Response
from rest_framework.views import APIView

from telebot import TeleBot
from telebot import types

from emoji import emojize

from .models import TelegramUser

TOKEN = 'TOKEN'

bot = TeleBot(TOKEN)
user = TelegramUser()

grin = emojize(':grin:', use_aliases=True)
 
class UpdateBot(APIView):
    def post(self, request):
        # Сюда должны получать сообщения от телеграм и далее обрабатываться ботом
        json_str = request.body.decode('UTF-8')
        update = types.Update.de_json(json_str)
        bot.process_new_updates([update])
 
        return Response({'code': 200})


@bot.message_handler(commands=['reg', 'register', 'start'])
def start(message):
	bot.send_message(message.chat.id, "Hello World!\n\n")
	msg = bot.reply_to(message, "To sign up, enter your username:")
	bot.register_next_step_handler(msg, sign_up_username)

def sign_up_username(message):
	try:
		if message.text != message.from_user.username:
			msg = bot.reply_to(message, "Enter your TELEGRAM username")
			bot.register_next_step_handler(msg, sign_up_username)
		else:
			user.username = message.text
			msg = bot.reply_to(message, "Great! Now enter your new password")
			bot.register_next_step_handler(msg, sign_up_password)
	except Exception as e:
		bot.reply_to(message, 'some error')
		print(e)

def sign_up_password(message):
	try:
		user.user_password = message.text
		msg = bot.reply_to(message, "OK! Confirm your password")
		bot.register_next_step_handler(msg, sign_up_confirm_password)
	except Exception as e:
		bot.reply_to(message, 'some error')
		print(e)

def sign_up_confirm_password(message):
	try:
		if message.text != user.user_password:
			msg = bot.reply_to(message, "Password unconfirmed! Try again!")
			bot.register_next_step_handler(msg, sign_up_confirm_password)
		else:
			user.user_id = message.from_user.id
			user.save()
			bot.send_message(message.chat.id, f'Congratulation! You\'re registered {grin}')
	except Exception as e:
		bot.reply_to(message, 'some error')
		print(e)

# Webhook
#bot.set_webhook(url="https://myapp.pythonanywhere.com/" + TOKEN)

bot.enable_save_next_step_handlers()
bot.load_next_step_handlers()

bot.polling()