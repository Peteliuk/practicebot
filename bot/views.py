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
TOKEN = 'TOKEN'

# Bot
bot = TeleBot(TOKEN)

# Modules
user = TelegramUser() # Telegram Users Module

# Emojis
grin = emojize(':grin:', use_aliases = True)
slightly_smilling_face = emojize(':slightly_smiling_face:', use_aliases = True)

# Telegram user (for checking of exsisting)
tguser = None

# User's task
task = None

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
	text = f'Hello {message.from_user.first_name} and welcome here!\n\n'
	text += 'To see some functions, type "/help" or "/Help"'
	bot.send_message(message.chat.id, text)

# Help command
@bot.message_handler(commands=['help', 'Help'])
def help(message):
	key = types.InlineKeyboardMarkup(row_width=3)
	key.add(types.InlineKeyboardButton('Sign Up', callback_data = 'sign_up'))
	key.add(types.InlineKeyboardButton('Sign In', callback_data = 'sign_in'))
	key.add(types.InlineKeyboardButton('Logout', callback_data = 'logout'))
	text = f'What can I do for you {slightly_smilling_face}? Check some functions {grin}'
	bot.send_message(message.chat.id, text, reply_markup=key)



@bot.callback_query_handler(func=lambda call: True)
def callback(call):
	try:
		# Telegram user (for checking of exsisting)
		global tguser
		tguser = TelegramUser.objects.filter(user_id = call.message.chat.id).first()
		if tguser:
			tguser.user_id = tguser.user_id
			tguser.name = tguser.name
			tguser.password = tguser.password
			tguser.loginned = tguser.loginned
			text = f'id: {tguser.user_id}\tname: {tguser.name}\n'
			text += f'password: {tguser.password}\tloginned: {tguser.loginned}'
			text += '\n----------------\n' 
			print(text)
		if call.message:
			if call.data == 'sign_up':
				if tguser:
					bot.send_message(call.message.chat.id, 'You are registered')
					if tguser.loginned:
						bot.send_message(call.message.chat.id, 'and signed in')
				else:
					text = "To sign up, enter your username:"
					msg = bot.send_message(call.message.chat.id, text)
					bot.register_next_step_handler(msg, sign_up_username)
			elif call.data == 'sign_in':
				if tguser:
					if tguser.loginned:
						bot.send_message(call.message.chat.id, 'You are signed in.')
					else:
						text = "To sign in, enter your username:"
						msg = bot.send_message(call.message.chat.id, text)
						bot.register_next_step_handler(msg, sign_in_username)
				else:
					text = "There are no account at database! Sign up first!\n"
					text += "To sign up, enter your username:"
					msg = bot.send_message(call.message.chat.id, text)
					bot.register_next_step_handler(msg, sign_up_username)
			elif call.data == 'logout':
				if tguser:
					if tguser.loginned:
						tguser.loginned = False
						tguser.save()
						bot.send_message(call.message.chat.id, 
							f'You have made logout! {slightly_smilling_face}')
					else:
						bot.send_message(call.message.chat.id, 'You\'re already unsigned in!')
				else:
					text = "There are no account at database! Sign up first!\n"
					text += "To sign up, enter your username:"
					msg = bot.send_message(call.message.chat.id, text)
					bot.register_next_step_handler(msg, sign_up_username)
			else:
				raise Exception()
	except Exception as e:
		bot.reply_to(call.message, 'some error')
		print(repr(e))
	
# Sign Up
def sign_up_username(message):
	try:
		if message.text != message.from_user.username:
			msg = bot.reply_to(message, "Enter your TELEGRAM username")
			bot.register_next_step_handler(msg, sign_up_username)
		else:
			user.name = message.text
			msg = bot.reply_to(message, "Great! Now enter your new password")
			bot.register_next_step_handler(msg, sign_up_password)
	except Exception as e:
		bot.reply_to(message, 'some error')
		print(repr(e))

def sign_up_password(message):
	try:
		user.password = message.text
		msg = bot.reply_to(message, "OK! Confirm your password")
		bot.register_next_step_handler(msg, sign_up_confirm_password)
	except Exception as e:
		bot.reply_to(message, 'some error')
		print(repr(e))

def sign_up_confirm_password(message):
	try:
		if message.text != user.password:
			msg = bot.reply_to(message, "Password unconfirmed! Try again!")
			bot.register_next_step_handler(msg, sign_up_confirm_password)
		else:
			user.user_id = message.from_user.id
			user.loginned = True
			user.save()
			bot.send_message(message.chat.id, f'Congratulation! You\'re registered {grin}')
	except Exception as e:
		bot.reply_to(message, 'some error')
		print(repr(e))


# Sign In
def sign_in_username(message):
	try:
		if message.text != tguser.name:
			msg = bot.reply_to(message, "Enter your TELEGRAM username")
			bot.register_next_step_handler(msg, sign_in_username)
		else:
			msg = bot.reply_to(message, "Great! Now enter your password")
			bot.register_next_step_handler(msg, sign_in_password)
	except Exception as e:
		bot.reply_to(message, 'some error')
		print(repr(e))

def sign_in_password(message):
	try:
		if message.text != tguser.password:
			msg = bot.reply_to(message, "Incorrected password! Try again:")
			bot.register_next_step_handler(msg, sign_in_password)
		else:
			tguser.loginned = True
			tguser.save()
			bot.send_message(message.chat.id, f'Congratulation! You\'re signed in {grin}')
	except Exception as e:
		bot.reply_to(message, 'some error')
		print(repr(e))


bot.enable_save_next_step_handlers()
bot.load_next_step_handlers()

bot.polling()