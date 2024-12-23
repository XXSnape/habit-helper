from telebot import TeleBot
from telebot.types import Message

from api.users.check_user import check_user_existence
from inline.keypads.cancel import get_cancel_kb
from states.auth import AuthStates
from utils.cache_keys import USERNAME_KEY, MESSAGE_ID_KEY


def validate_username_and_request_password(message: Message, bot: TeleBot) -> None:
    """
    Проверяет, существует ли уже пользователь с таким username.
    Запрашивает пароль для продолжения регистрации
    :param message: Message
    :param bot: TeleBot
    """
    username = message.text
    is_existing = check_user_existence(username)
    if is_existing:
        bot.send_message(
            message.chat.id,
            f"К сожалению, пользователь {username} уже существует. Напишите другой никнейм",
            reply_markup=get_cancel_kb(),
        )
        return
    sent_message = bot.send_message(
        message.chat.id,
        f"Отлично! Ваш потенциальный никнейм: {username}. Теперь нужно ввести пароль.\n",
        reply_markup=get_cancel_kb(),
    )
    with bot.retrieve_data(sent_message.chat.id, sent_message.chat.id) as data:
        data[USERNAME_KEY] = username
        data[MESSAGE_ID_KEY] = sent_message.id
    bot.set_state(
        user_id=message.chat.id,
        chat_id=message.chat.id,
        state=AuthStates.password,
    )


def register_password(bot: TeleBot) -> None:
    """
    Регистрирует validate_username_and_request_password
    :param bot: TeleBot
    """
    bot.register_message_handler(
        validate_username_and_request_password,
        pass_bot=True,
        state=AuthStates.username,
    )
