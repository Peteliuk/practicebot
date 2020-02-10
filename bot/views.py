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
bot = TeleBot(TOKEN, threaded=False)

# Emojis
grin = emojize(':grin:', use_aliases=True)
slightly_smiling_face = emojize(':slightly_smiling_face:', use_aliases=True)
x = emojize(':x:', use_aliases=True)
white_check_mark = emojize(':white_check_mark:', use_aliases=True)
sign_of_the_horns = emojize(':sign_of_the_horns:', use_aliases=True)

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
	# if tg_id field equals None, telegram user isn't signed in
	# if tg_id field equals telegram user's id, he or she is signed in
	query = TelegramUser.objects.filter(tg_id=message.from_user.id).first()
	if query:
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
	text = "<b>BVBlogic Bot</b> - telegram bot for practice in <i>BVBlogic company</i>\n"
	text += "You can watch your tasks. To do this, type /tasks command\n\n"
	text += "developed by <a href='https://t.me/liubomyr'>Liubomyr Peteliuk</a> \n"
	text += "Project code on <a href='https://github.com/Peteliuk/practicebot'>Github</a> "
	bot.send_message(message.chat.id, text, parse_mode='HTML')

# Tasks command
@bot.message_handler(commands=['tasks', 'Tasks'])
def tasks(message):
	query = TelegramUser.objects.filter(tg_id=message.from_user.id).first()
	if query:
		if query.task_set.first():
			key = types.InlineKeyboardMarkup()
			for task in query.task_set.all():
				key.add(types.InlineKeyboardButton(task.name, callback_data=task.id))
			bot.send_message(message.chat.id, 'Your tasks:\n', reply_markup=key)
		else:
			bot.send_message(message.chat.id, f'You haven\'t any task {sign_of_the_horns}')
	else:
		text = f'To see your tasks sign in at first\n tap your login:'
		msg = bot.send_message(message.chat.id, text)
		bot.register_next_step_handler(msg, sign_in_username)

# Callback handler
@bot.callback_query_handler(func=lambda call: True)
def callback(call):
	if call.data.isdigit():
		task = Task.objects.filter(id=call.data).first()
		text = f"<b>Name:</b>\t<i>{task.name}</i>\n\n"
		text += f"<b>Description:</b>\n<i>{task.description}</i>\n"
		task_status = 'None'
		if task.acceed is not None:
			task_status = f'{white_check_mark} <i>acepted</i>' if task.acceed else f'{x} <i>rejected</i>'
		if task.complited:
			task_status = f'{sign_of_the_horns} complited'
		text += f"\n<b>Status</b>: <i>{task_status}</i>"
		key = types.InlineKeyboardMarkup()
		reject = types.InlineKeyboardButton(f'{x} reject', callback_data=f'reject {call.data}')
		accept = types.InlineKeyboardButton(f'{white_check_mark} accept', callback_data=f'accept {call.data}')
		''' Don't show inline keyboard if task is complited or acepted or rejected '''
		if not (task.acceed is not None or task.complited): 
			key.row(reject, accept)
		bot.send_message(call.message.chat.id, text, parse_mode='HTML', reply_markup=key)
	else:
		''' Inline keyboard's callback data looks like "command task_id" '''
		task_id = int(call.data.split()[1])
		command = call.data.split()[0]
		task = Task.objects.filter(id=task_id).first()
		if command == 'reject':
			task.acceed = False			
			task.save()
			text = f'Task <i>{task.name}</i> {x} rejected!'
			bot.delete_message(call.message.chat.id, call.message.message_id)
			bot.send_message(call.message.chat.id, text, parse_mode='HTML')
		elif command == 'accept':
			task.acceed = True
			task.save()
			text = f'Task <i>{task.name}</i> {white_check_mark} acepted!'
			bot.delete_message(call.message.chat.id, call.message.message_id)
			bot.send_message(call.message.chat.id, text, parse_mode='HTML')
		else:
			bot.send_message(call.message.chat.id, 'some error')
		
# Sign In
def sign_in_username(message):
	try:
		tguser = TelegramUser.objects.filter(login=message.text).first()
		if tguser:
			msg = bot.reply_to(message, "Great! Now enter your password:")
			bot.register_next_step_handler(msg, sign_in_password, tguser)
		else:
			msg = bot.reply_to(message, "Incorrect login! Try again:")
			bot.register_next_step_handler(msg, sign_in_username)
	except Exception as e:
		bot.reply_to(message, 'some error')
		print(repr(e))

def sign_in_password(message, tguser):
	try:
		if message.text == tguser.password:
			tguser.tg_id = message.from_user.id
			tguser.save()
			bot.send_message(message.chat.id, f'Congratulation! You\'re signed in {grin}')
		else:
			msg = bot.reply_to(message, "Incorrected password! Try again:")
			bot.register_next_step_handler(msg, sign_in_password, tguser)
	except Exception as e:
		bot.reply_to(message, 'some error')
		print(repr(e))


bot.enable_save_next_step_handlers(delay=2)
bot.load_next_step_handlers()

# for localhost (delete it if you want to deploy)
# bot.polling()
