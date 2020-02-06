#from django.shortcuts import render
from django.conf import settings

from rest_framework.response import Response
from rest_framework.views import APIView

from telebot import TeleBot
from telebot import types

from emoji import emojize

from .models import TelegramUser
from .models import Task

# Bot token
TOKEN = 'Say my name ))'

# Bot
bot = TeleBot(TOKEN)

# Emojis
grin = emojize(':grin:', use_aliases = True)
slightly_smiling_face = emojize(':slightly_smiling_face:', use_aliases = True)

# For reading response text from telegram server
class UpdateBot(APIView):
	def post(self, request):        
		json_str = request.body.decode('UTF-8')
		update = types.Update.de_json(json_str)
		bot.process_new_updates([update])

		return Response({'code': 200})

# Start command
@bot.message_handler(commands=['start', 'Start'])
def start(message):
	# if user_id field equals None, telegram user isn't signed in
	# if user_id field equals telegram user's id, he or she is signed in
	tguser = TelegramUser.objects.filter(user_id=message.from_user.id).first()
	if tguser:
		text = f'Hello {message.from_user.first_name}, how are you? {slightly_smiling_face}\n'
		text += 'To see more information, type "/help" or "/Help"'
		bot.send_message(message.chat.id, text)
	else:
		text = f'Hello {message.from_user.first_name}, how are you? {slightly_smiling_face}\n'
		text = f'To use the bot enter your login plz {slightly_smiling_face}:'
		msg = bot.send_message(message.chat.id, text)
		bot.register_next_step_handler(msg, sign_in_username)

# Help command
@bot.message_handler(commands=['help', 'Help'])
def help(message):
	bot.send_message(message.chat.id, f'In development {grin}.')

# Sign In
def sign_in_username(message):
	try:
		tguser = TelegramUser.objects.filter(login=message.text).first()
		if tguser:
			msg = bot.reply_to(message, "Great! Now enter your password:")
			bot.register_next_step_handler(msg, lambda m: sign_in_password(m, tguser))
		else:
			msg = bot.reply_to(message, "Incorrect login! Try again:")
			bot.register_next_step_handler(msg, sign_in_username)
	except Exception as e:
		bot.reply_to(message, 'some error')
		print(repr(e))

def sign_in_password(message, tguser):
	try:
		if message.text == tguser.password:
			tguser.user_id = message.from_user.id
			tguser.save()
			bot.send_message(message.chat.id, f'Congratulation! You\'re signed in {grin}')
		else:
			msg = bot.reply_to(message, "Incorrected password! Try again:")
			bot.register_next_step_handler(msg, sign_in_password)
	except Exception as e:
		bot.reply_to(message, 'some error')
		print(repr(e))


bot.enable_save_next_step_handlers()
bot.load_next_step_handlers()

#bot.polling()