from telebot import TeleBot

from telebot.types import Message

from database.crud.check_user import get_user_token
from inline.keypads.auth import get_auth_request_kb
from utils.texts import COMMANDS


def start(message: Message, bot: TeleBot) -> None:
    """
    Обрабатывает команду /start
    :param message: Message
    :param bot: TeleBot
    """
    token = get_user_token(telegram_id=message.chat.id)
    if token is None:
        bot.send_message(
            message.chat.id,
            f"Здравствуйте, {message.from_user.first_name}!\n"
            f"Я помогу удобно отслеживать привычки и напоминать о них.\n"
            f"Но для начала нужно пройти регистрацию, чтобы мной можно было пользоваться"
            f"на любом аккаунте в телеграм",
            reply_markup=get_auth_request_kb(),
        )
        return
    bot.send_message(message.chat.id, text=COMMANDS)


def register_start(bot: TeleBot) -> None:
    """
    Регистрирует start
    :param bot: TeleBot
    """
    bot.register_message_handler(start, commands=["start"], pass_bot=True)
