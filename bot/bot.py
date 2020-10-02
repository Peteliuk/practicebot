import logging

from django.contrib.auth.hashers import check_password

from telebot import TeleBot
from telebot import types
from telebot import logger

from bot.constants import strings
from bot.constants import emojis

from .models import TelegramUser
from .models import Task

# Bot
bot = TeleBot(strings.TOKEN, threaded=False)

# Outputs debug messages to console.
logger.setLevel(logging.DEBUG)


# Start command
@bot.message_handler(commands=strings.start_cmd)
def start_command(message):
    """
    if telegram_id field equals None, telegram user isn't signed in.
    if telegram_id field equals telegram user's id, he or she is signed in
    """
    # Get telegram user by telegram id
    user = TelegramUser.objects.get_telegram_user(telegram_id=message.from_user.id)
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
    user = TelegramUser.objects.get_telegram_user(telegram_id=message.from_user.id)
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
    bot.send_message(message.chat.id, text='Keyboard removed', reply_markup=types.ReplyKeyboardRemove())


# Show information about chosen task
@bot.message_handler(func=lambda msg: message_text_is_task_id(msg))
def choose_task(message):
    task = Task.objects.get(id=message.text)
    text = f"<b>Name:</b>\t<i>{task.name}</i>\n\n" \
           f"<b>Description:</b>\n<i>{task.description}</i>\n\n" \
           f"<b>Date</b>\t<i>{task.date.strftime('%d %B %Y')}</i>\n\n" \
           f"<b>Status</b>: <i>{task.get_status_display()}</i>"
    markup = types.ReplyKeyboardRemove()
    if task.status == 1:
        markup = types.InlineKeyboardMarkup()
        markup.row(
            types.InlineKeyboardButton(f'{emojis.x} reject {task.id}', callback_data=f'{strings.reject} {task.id}'),
            types.InlineKeyboardButton(f'{emojis.white_check_mark} accept {task.id}',
                                       callback_data=f'{strings.accept} {task.id}'
                                       ),
        )
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
    user = TelegramUser.objects.get_telegram_user(telegram_id=call.message.chat.id)
    if not user:
        bot.send_message(call.message.chat.id, 'Your user data does not exist! Maybe it was deleted! Type /start')
        return
    show_tasks(call.message.chat.id, call.message.message_id, 'Future tasks are showed',
               Task.objects.get_future_tasks, user.id)


# Show past tasks
@bot.callback_query_handler(func=lambda call: strings.past_tasks in call.data)
def show_past_tasks(call):
    user = TelegramUser.objects.get_telegram_user(telegram_id=call.message.chat.id)
    if not user:
        bot.send_message(call.message.chat.id, 'Your user data does not exist! Maybe it was deleted! Type /start')
        return
    show_tasks(call.message.chat.id, call.message.message_id, 'Past tasks are showed',
               Task.objects.get_past_tasks, user.id)


# Reject task
@bot.callback_query_handler(func=lambda call: strings.reject in call.data)
def reject_task(call):
    set_task_status(call.message.chat.id, call.message.message_id, int(call.data.split()[1]), 2, f'Rejected {emojis.x}')


# Accept task
@bot.callback_query_handler(func=lambda call: strings.accept in call.data)
def accept_task(call):
    set_task_status(call.message.chat.id, call.message.message_id,
                    int(call.data.split()[1]), 3, f'Accepted {emojis.white_check_mark}')


# Sign In
def sign_in_email(message):
    """
    User must enter email.
    User will be able to enter password, if gets TelegramUser object,
    else will enter email again
    """
    # Get telegram user by email
    user = TelegramUser.objects.get_telegram_user(email=message.text)
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
    user = TelegramUser.objects.get_telegram_user(id=user_id)
    if not check_password(message.text, user.password):
        return bot.register_next_step_handler(
            bot.reply_to(message, "Incorrect password! Try again:"),
            sign_in_password, user.id,
        )
    TelegramUser.objects.set_telegram_user_telegram_id(user_id, message.from_user.id)
    bot.send_message(message.chat.id, f'Congratulation! You\'re signed in {emojis.grin}')


# Check if message text is task id
def message_text_is_task_id(message):
    """
    Returns False if user isn't signed in and if message.text is not digit
    Returns True if converted to int message text is in list of tasks ids
    """
    user = TelegramUser.objects.get_telegram_user(telegram_id=message.from_user.id)
    if not (user and message.text.isdigit()):
        return False
    tasks_ids_list = Task.objects.get_all_tasks_ids_list(user.id)
    return int(message.text) in tasks_ids_list


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


def set_task_status(chat_id, message_id, task_id, status, text):
    """
    Changes task status:
        values:
            1 - Created
            2 - Rejected
            3 - Accepted
            4 - Completed
        Notice: from bot you can accept or reject task

    Checks if task exists

    :param chat_id:             message's chat id
    :param message_id:          message's id (uses to change task information message
                                to notification about task status changing to accepted or rejected
    :param task_id:             id of task what might be changed
    :param status:              task's status number (int)
    :param text:                text that notified user about rejecting or accepting task
    """
    if not Task.objects.get(id=task_id):
        bot.send_message(chat_id, 'Your task data does not exist! Maybe it was deleted! Type /tasks')
        return
    Task.objects.set_task_status(task_id, status)
    bot.edit_message_text(text, chat_id, message_id)


bot.enable_save_next_step_handlers()
bot.load_next_step_handlers()
