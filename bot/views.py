from rest_framework.response import Response
from rest_framework.views import APIView

from telebot import TeleBot
from telebot import types

from emoji import emojize

from .modules.user_module import UserModule as um

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

# Cache
cache = {}

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
	'''
	if tg_id field equals None, telegram user isn't signed in
	if tg_id field equals telegram user's id, he or she is signed in
	'''
	
	user_id = um().get_tguser_id(tg_id=message.from_user.id)
	if not user_id:
		return autorize(message, 
			f'To use the bot enter your login plz {slightly_smiling_face}:',
			sign_in_login
		)
	text = f'Hello {message.from_user.first_name}, how are you? {slightly_smiling_face}\n' \
		   f'To see more information, type "/help" or "/Help"'
	cache['user_id'] = user_id
	bot.send_message(message.chat.id, text)

# Help command
@bot.message_handler(commands=['help', 'Help'])
def help(message):
	text = "<b>BVBlogic Bot</b> - telegram bot for practice in <i>BVBlogic company</i>\n" \
		   "You can watch your tasks. To do this, type /tasks command\n\n" \
		   "developed by <a href='https://t.me/liubomyr'>Liubomyr Peteliuk</a> \n" \
		   "Project code on <a href='https://github.com/Peteliuk/practicebot'>Github</a> "
	bot.send_message(message.chat.id, text, parse_mode='HTML')

# Tasks command
@bot.message_handler(commands=['tasks', 'Tasks'])
def tasks(message):
	pass

# Sign In
def sign_in_login(message):
	'''
	User must enter his or her login.
	If user gets his id from database, he or she will be able to enter password,
	else user will enter login again
	'''

	try:
		user_id = um().get_tguser_id(login=message.text)
		if not user_id:
			return autorize(message, "Incorrect login! Try again:", sign_in_login)
		autorize(message, "Great! Now enter your password:", sign_in_password, user_id)
	except Exception as e:
		bot.reply_to(message, 'some error')
		print(repr(e))

def sign_in_password(message, user_id):
	'''
	User must type his or her password.
	If user types correct password, he or she will be signed in,
	else user will enter password again
	'''
	
	try:
		tguser = um().get_tguser(user_id)

		if message.text != tguser.password:
			return autorize(message, "Incorrected password! Try again:", 
				sign_in_password, user_id
			)
		um().set_tguser_tg_id(user_id, message.from_user.id)
		cache['user_id'] = user_id
		bot.send_message(message.chat.id, f'Congratulation! You\'re signed in {grin}')
	except Exception as e:
		bot.reply_to(message, 'some error')
		print(repr(e))


def autorize(message, text, callback_func, *args):
	'''
	Registers a callback function to be notified when new message arrives after `message`.
	
	Warning: In case `callback` as lambda function, saving next step handlers will not work.

	:param message:		The message for which we want to handle new message in the same chat.
	:param text:		Text what will be showed in `callback`
	:param callback:	The callback function which next new message arrives.
	:param args:		Args to pass in callback func
	'''
	msg = bot.send_message(message.chat.id, text)
	bot.register_next_step_handler(msg, callback_func, *args)


bot.enable_save_next_step_handlers()
bot.load_next_step_handlers()

# for localhost (delete it if you want to deploy)
bot.polling()
