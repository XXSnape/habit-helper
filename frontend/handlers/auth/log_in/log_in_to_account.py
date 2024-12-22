from telebot import TeleBot
from telebot.types import Message

from api.users.change_telegram_id import change_telegram_id_by_credentials
from states.auth import LogInStates
from utils.cache_keys import USERNAME_KEY, MESSAGE_ID_KEY
from utils.regexp import PASSWORD_REGEXP
from utils.texts import COMMANDS, DELETE_PASSWORD


def log_in(message: Message, bot: TeleBot) -> None:
    """
    Логинит пользователя в существующий аккаунт.
    :param message: Message
    :param bot: TeleBot
    """
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
        bot.send_message(message.chat.id, text=COMMANDS)
        return
    bot.send_message(
        message.chat.id,
        f"Успешная авторизация!\n{DELETE_PASSWORD}",
    )
    bot.send_message(message.chat.id, text=COMMANDS)


def register_log_in(bot: TeleBot) -> None:
    """
    Регистрирует log_in
    :param bot: TeleBot
    """
    bot.register_message_handler(
        log_in,
        pass_bot=True,
        state=LogInStates.password,
        regexp=PASSWORD_REGEXP,
    )
