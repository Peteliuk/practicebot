import logging

from django.contrib.auth.hashers import check_password

from rest_framework.response import Response
from rest_framework.views import APIView

from telebot import TeleBot
from telebot import types
from telebot import logger

from .user_module import UserModule as um
from .task_module import TaskModule as tm

from bot.constants import strings
from bot.constants import emojis

# Bot
bot = TeleBot(strings.TOKEN, threaded=False)

# Outputs debug messages to console.
logger.setLevel(logging.DEBUG)


# For reading response text from telegram server
class UpdateBot(APIView):
    def post(self, request):
        json_str = request.body.decode('UTF-8')
        update = types.Update.de_json(json_str)
        bot.process_new_updates([update])

        return Response({'code': 200})


# Start command
@bot.message_handler(commands=strings.start_cmd)
def start_command(message):
    """
    if telegram_id field equals None, telegram user isn't signed in.
    if telegram_id field equals telegram user's id, he or she is signed in
    """
    # Get telegram user by telegram id
    user = um().get_telegram_user(telegram_id=message.from_user.id)
    if not user:
        return bot.register_next_step_handler(
            bot.reply_to(message, 'To use bot, enter your email first'),
            sign_in_email,
        )
    text = f'Hello {message.from_user.first_name}, how are you? {emojis.slightly_smiling_face}\n' \
           'To see more information, type "/help" or "/Help"'
    bot.send_message(message.chat.id, text)


# Help command
@bot.message_handler(commands=strings.help_cmd)
def help_command(message):
    text = "<b>BVBlogic Bot</b> - telegram bot for practice in <i>BVBlogic company</i>\n" \
           "You can watch your tasks. To do this, type /tasks command\n\n" \
           "developed by <a href='https://t.me/liubomyr'>Liubomyr Peteliuk</a> \n" \
           "Project code on <a href='https://github.com/Peteliuk/practicebot'>Github</a> "
    bot.send_message(message.chat.id, text, parse_mode='HTML')


# Tasks command
@bot.message_handler(commands=strings.tasks_cmd)
def tasks_command(message):
    user = um().get_telegram_user(telegram_id=message.from_user.id)
    if not user:
        return bot.register_next_step_handler(
            bot.reply_to(message, 'To use bot, enter your email first'),
            sign_in_email,
        )
    markup = types.InlineKeyboardMarkup()
    markup.row(
        types.InlineKeyboardButton('Future tasks', callback_data='future tasks'),
        types.InlineKeyboardButton('Past tasks', callback_data='past tasks')
    )
    bot.send_message(message.chat.id, 'If you want to remove keyboard, type /rmkeyboard', reply_markup=markup)


# Remove keyboard command
@bot.message_handler(commands=strings.remove_keyboard_cmd)
def remove_keyboard_command(message):
    markup = types.ReplyKeyboardRemove()
    bot.send_message(message.chat.id, text='Keyboard removed', reply_markup=markup)


# Show information about chosen task
@bot.message_handler(func=lambda msg: message_text_is_task_id(msg))
def choose_task(message):
    task = tm().get_task(message.text)
    text = f"<b>Name:</b>\t<i>{task.name}</i>\n\n" \
           f"<b>Description:</b>\n<i>{task.description}</i>\n\n" \
           f"<b>Date</b>\t<i>{task.date.strftime('%d %B %Y')}</i>\n\n" \
           f"<b>Status</b>: <i>{task.get_status_display()}</i>"
    markup = types.InlineKeyboardMarkup()
    markup.row(
        types.InlineKeyboardButton(f'{emojis.x} reject {task.id}', callback_data=f'{strings.reject} {task.id}'),
        types.InlineKeyboardButton(f'{emojis.white_check_mark} accept {task.id}',
                                   callback_data=f'{strings.accept} {task.id}'
                                   ),
    )
    # Dont show `reject` and `accept` buttons if task has not `created` status
    if task.status != 1:
        markup = None
    msg = bot.send_message(message.chat.id, 'Wait...', reply_markup=types.ReplyKeyboardRemove())
    bot.delete_message(message.chat.id, msg.message_id)
    bot.send_message(message.chat.id, text, parse_mode='HTML', reply_markup=markup)


# Back command
@bot.message_handler(func=lambda msg: strings.back in msg.text)
def back_command(message):
    bot.delete_message(message.chat.id, message.message_id)
    tasks_command(message)


# Unknown command
@bot.message_handler(func=lambda msg: True)
def unknown_command(message):
    bot.send_message(message.chat.id, f'Unknown command {emojis.confused}')


# Show future tasks
@bot.callback_query_handler(func=lambda call: strings.future_tasks in call.data)
def show_future_tasks(call):
    user = um().get_telegram_user(telegram_id=call.message.chat.id)
    show_tasks(call.message.chat.id, call.message.message_id, 'Future tasks are showed', tm().get_future_tasks, user.id)


# Show past tasks
@bot.callback_query_handler(func=lambda call: strings.past_tasks in call.data)
def show_past_tasks(call):
    user = um().get_telegram_user(telegram_id=call.message.chat.id)
    show_tasks(call.message.chat.id, call.message.message_id, 'Past tasks are showed', tm().get_past_tasks, user.id)


# Reject task
@bot.callback_query_handler(func=lambda call: strings.reject in call.data)
def reject_task(call):
    task_id = int(call.data.split()[1])
    tm().set_task_status(task_id, 2)
    bot.edit_message_text(f'Rejected {emojis.x}', call.message.chat.id, call.message.message_id)


# Accept task
@bot.callback_query_handler(func=lambda call: strings.accept in call.data)
def accept_task(call):
    task_id = int(call.data.split()[1])
    tm().set_task_status(task_id, 3)
    bot.edit_message_text(f'Accepted {emojis.white_check_mark}', call.message.chat.id, call.message.message_id)


# Sign In
def sign_in_email(message):
    """
    User must enter email.
    User will be able to enter password, if gets TelegramUser object,
    else will enter email again
    """
    # Get telegram user by email
    user = um().get_telegram_user(email=message.text)
    # If user is not exist or has already filled telegram id field
    if not user or user.telegram_id:
        return bot.register_next_step_handler(
            bot.reply_to(message, 'Incorrect email! Try again:'),
            sign_in_email,
        )
    bot.register_next_step_handler(
        bot.reply_to(message, "Great! Now enter your password:"),
        sign_in_password, user.id,
    )


def sign_in_password(message, user_id):
    """
    User must type password.
    User will be signed in, if types correct password,
    else will enter password again
    """
    # Get telegram user by id in database
    user = um().get_telegram_user(user_id=user_id)
    if not check_password(message.text, user.password):
        return bot.register_next_step_handler(
            bot.reply_to(message, "Incorrect password! Try again:"),
            sign_in_password, user.id,
        )
    um().set_telegram_user_telegram_id(user_id, message.from_user.id)
    bot.send_message(message.chat.id, f'Congratulation! You\'re signed in {emojis.grin}')


# Check if message text is task id
def message_text_is_task_id(msg):
    user = um().get_telegram_user(telegram_id=msg.from_user.id)
    if not user:
        return
    tasks_ids_list = tm().get_all_tasks_ids_list(user.id)
    return msg.text in tasks_ids_list


def show_tasks(chat_id, message_id, text, func, user_id):
    """
    Shows tasks list by callback function and user's id.

    :param chat_id:         Chat id
    :param message_id:      Message id
    :param text:            Text what bot will send
    :param func:            The function what will be performed: get_future_tasks or get_past_tasks
    :param user_id:         User's id that provides us information for what user we must take tasks
    """
    tasks = func(user_id)
    if not tasks:
        return bot.send_message(chat_id, f'{emojis.sign_of_the_horns} no tasks')
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=5)
    markup.add(*[types.KeyboardButton(text=f'{el.id}') for el in tasks],
               types.KeyboardButton(text=f'{emojis.arrow_left} {strings.back}'),
               )
    bot.delete_message(chat_id, message_id)
    bot.send_message(chat_id, text, reply_markup=markup)


bot.enable_save_next_step_handlers()
bot.load_next_step_handlers()
