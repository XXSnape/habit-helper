from telebot import TeleBot

from telebot.types import Message
from keyboards.inline.keypads.auth import get_auth_request_kb


def start(message: Message, bot: TeleBot):
    bot.send_message(
        message.chat.id,
        f"Здравствуйте, {message.from_user.first_name}!\n"
        f"Я помогу удобно отслеживать привычки и напоминать о них.\n"
        f"Но для начала нужно пройти регистрацию, чтобы мной можно было пользоваться"
        f"на любом аккаунте в телеграм",
        reply_markup=get_auth_request_kb(),
    )


def register_help(bot: TeleBot) -> None:
    bot.register_message_handler(start, commands=["start"], pass_bot=True)
