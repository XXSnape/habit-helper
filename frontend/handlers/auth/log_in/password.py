from telebot import TeleBot
from telebot.types import Message

from inline.keypads.cancel import get_cancel_kb
from states.auth import LogInStates
from utils.cache_keys import USERNAME_KEY, MESSAGE_ID_KEY


def get_password_to_login_to_another_account(message: Message, bot: TeleBot):
    username = message.text
    bot.set_state(
        user_id=message.chat.id,
        chat_id=message.chat.id,
        state=LogInStates.password,
    )
    sent_message = bot.send_message(
        message.chat.id,
        "Введите пароль\n",
        reply_markup=get_cancel_kb(),
    )
    with bot.retrieve_data(message.chat.id, message.chat.id) as data:
        data[USERNAME_KEY] = username
        data[MESSAGE_ID_KEY] = sent_message.id


def register_log_in_password(bot: TeleBot):
    bot.register_message_handler(
        get_password_to_login_to_another_account,
        state=LogInStates.username,
        pass_bot=True,
    )
