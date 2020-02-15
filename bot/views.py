from rest_framework.response import Response
from rest_framework.views import APIView

from telebot import TeleBot
from telebot import types

from emoji import emojize

from .modules.user_module import UserModule as um
from .modules.task_module import TaskModule as tm

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

# Status values
status_values = {
    '1': 'None',
    '2': f'{x} rejected',
    '3': f'{white_check_mark} accepted',
    '4': f'{sign_of_the_horns} completed'
}


# For reading response text from telegram server
class UpdateBot(APIView):
    def post(self, request):
        json_str = request.body.decode('UTF-8')
        update = types.Update.de_json(json_str)
        bot.process_new_updates([update])

        return Response({'code': 200})


# Start command
@bot.message_handler(commands=['start', 'Start'])
def start_cmd(message):
    """
    if tg_id field equals None, telegram user isn't signed in.
    if tg_id field equals telegram user's id, he or she is signed in
    """
    user_id = um().get_tguser_id(tg_id=message.from_user.id)
    if not user_id:
        return autorize(message.chat.id,
                        f'To use the bot enter your login plz {slightly_smiling_face}:',
                        sign_in_login
                        )
    text = f'Hello {message.from_user.first_name}, how are you? {slightly_smiling_face}\n' \
           f'To see more information, type "/help" or "/Help"'
    cache['user_id'] = user_id
    bot.send_message(message.chat.id, text)


# Help command
@bot.message_handler(commands=['help', 'Help'])
def help_cmd(message):
    text = "<b>BVBlogic Bot</b> - telegram bot for practice in <i>BVBlogic company</i>\n" \
           "You can watch your tasks. To do this, type /tasks command\n\n" \
           "developed by <a href='https://t.me/liubomyr'>Liubomyr Peteliuk</a> \n" \
           "Project code on <a href='https://github.com/Peteliuk/practicebot'>Github</a> "
    bot.send_message(message.chat.id, text, parse_mode='HTML')


# Tasks command
@bot.message_handler(commands=['tasks', 'Tasks'])
def tasks_cmd(message):
    user_id = um().get_tguser_id(tg_id=message.from_user.id)
    if not user_id:
        return autorize(message.chat.id, f'To see your tasks sign in at first.\nTap your login:', sign_in_login)
    cache['user_id'] = user_id
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.row(types.KeyboardButton('Future tasks'), types.KeyboardButton('Past tasks'))
    bot.send_message(message.chat.id, 'If you want to remove keyboard, type /rmkeyboard', reply_markup=markup)


# Remove keyboard command
@bot.message_handler(commands=['rmkeyboard'])
def rmkeyboard_cmd(message):
    markup = types.ReplyKeyboardRemove()
    bot.send_message(message.chat.id, text='Keyboard removed', reply_markup=markup)


# Show Tasks options Message handler
@bot.message_handler(func=lambda msg: msg.text in ['Future tasks', 'Past tasks'])
def tasks_options(message):
    if message.text == 'Past tasks':
        return show_tasks(message.chat.id, 'Past tasks are showed', tm().get_past_tasks, cache.get('user_id'))
    show_tasks(message.chat.id, 'Future tasks are showed', tm().get_future_tasks, cache.get('user_id'))


# Show information about chosen task
@bot.message_handler(func=lambda msg: msg.text in [str(el.id) for el in tm().get_all_tasks(cache.get('user_id'))])
def choose_task(message):
    bot.delete_message(message.chat.id, message.message_id)
    task = tm().get_task(message.text)
    text = f"<b>Name:</b>\t<i>{task.name}</i>\n\n" \
           f"<b>Description:</b>\n<i>{task.description}</i>\n\n" \
           f"<b>Status</b>: <i>{status_values.get(str(task.status))}</i>"
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.row(
        types.KeyboardButton(text=f'{x} reject {task.id}'),
        types.KeyboardButton(text=f'{white_check_mark} accept {task.id}')
    )
    # Dont show `reject` and `accept` buttons if task has not None status
    if task.status != 1:
        markup = cache.get('markup')
    msg = bot.send_message(message.chat.id, text, reply_markup=markup, parse_mode='HTML')
    cache['msg_id'] = msg.message_id


# Update chosen task
@bot.message_handler(func=lambda msg: msg.text.split()[1] in ['reject', 'accept'])
def update_chosen_task(message):
    """
    Handle messages what second word is `reject` or 'accept'.
    Message text structure: `emoji command task_id`
    Status variants:
        1: None
        2: Rejected
        3: Accepted
        4: Completed
    """
    command = message.text.split()[1]
    task_id = int(message.text.split()[2])
    if command == 'reject':
        return change_task_status(message.chat.id, f'Rejected {x}', task_id, 2)
    change_task_status(message.chat.id, f'Accepted {white_check_mark}', task_id, 3)


# Sign In
def sign_in_login(message):
    """
    User must enter his or her login.
    If user gets his id from database, he or she will be able to enter password,
    else user will enter login again
    """
    try:
        user_id = um().get_tguser_id(login=message.text)
        if not user_id:
            return autorize(message.chat.id, "Incorrect login! Try again:", sign_in_login)
        autorize(message.chat.id, "Great! Now enter your password:", sign_in_password, user_id)
    except Exception as e:
        bot.reply_to(message, 'some error')
        print(repr(e))


def sign_in_password(message, user_id):
    """
    User must type his or her password.
    If user types correct password, he or she will be signed in,
    else user will enter password again
    """
    try:
        tguser = um().get_tguser(user_id)
        if message.text != tguser.password:
            return autorize(message.chat.id, "Incorrect password! Try again:",
                            sign_in_password, user_id
                            )
        um().set_tguser_tg_id(user_id, message.from_user.id)
        cache['user_id'] = user_id
        bot.send_message(message.chat.id, f'Congratulation! You\'re signed in {grin}')
    except Exception as e:
        bot.reply_to(message, 'some error')
        print(repr(e))


def autorize(chat_id, text, callback_func, *args):
    """
    Warning: In case `callback` as lambda function, saving next step handlers will not work.

    :param chat_id:			Message chat id.
    :param text:			Text what bot will send.
    :param callback_func:	The callback function which next new message arrives.
    :param args:			Args to pass in callback func.
    """
    msg = bot.send_message(chat_id, text)
    bot.register_next_step_handler(msg, callback_func, *args)


def show_tasks(chat_id, text, func, user_id):
    """
    Shows tasks list by callback function and user's id.

    :param chat_id:         Message chat id
    :param text:            Text what bot will send
    :param func:            The function what will be performed
    :param user_id:         User's id that provides us information for what user we must take tasks
    """
    tasks = func(user_id)
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=5)
    buttons = []
    for el in tasks:
        buttons.append(types.KeyboardButton(text=f'{el.id}'))
    markup.add(*buttons)
    cache['markup'] = markup
    bot.send_message(chat_id=chat_id, text=text, reply_markup=markup)


def change_task_status(chat_id, text, task_id, task_status):
    """
    Changes selected task status and edit message

    :param chat_id:         Message chat id
    :param text:            Text what bot will send
    :param task_id:         Selected task id
    :param task_status:     Selected task status
    """
    tm().set_task_status(task_id, task_status)
    bot.delete_message(chat_id, cache.get('msg_id'))
    bot.send_message(chat_id, text, reply_markup=cache.get('markup'))


bot.enable_save_next_step_handlers()
bot.load_next_step_handlers()

# for localhost (delete it if you want to deploy)
bot.polling(none_stop=True)
