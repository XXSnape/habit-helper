from telebot import TeleBot
from telebot.types import Message

from api.users.change_telegram_id import change_telegram_id_by_credentials
from states.auth import LogInStates
from utils.constants import USERNAME_KEY, MESSAGE_ID_KEY


def log_in(message: Message, bot: TeleBot):
    password = message.text
    with bot.retrieve_data(message.chat.id, message.chat.id) as data:
        username = data[USERNAME_KEY]
        message_id = data[MESSAGE_ID_KEY]
    result = change_telegram_id_by_credentials(
        username=username, password=password, new_telegram_id=message.chat.id
    )
    bot.delete_state(message.chat.id, message.chat.id)
    bot.delete_message(message.chat.id, message_id)
    if result is False:
        bot.send_message(message.chat.id, "Неверный никнейм или пароль")
        return
    bot.send_message(
        message.chat.id,
        "Успешная авторизация!\nПожалуйста, запомните свой пароль и удалите его из переписки",
    )


def register_log_in(bot: TeleBot):
    bot.register_message_handler(log_in, pass_bot=True, state=LogInStates.password)
