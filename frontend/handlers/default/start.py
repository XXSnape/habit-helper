from telebot import TeleBot

from frontend.loader import bot
from telebot.types import Message


@bot.message_handler(commands=["start"])
def start(message: Message):
    bot.send_message(
        message.chat.id,
        f"Здравствуйте, {message.from_user.first_name}!\n"
        f"Я помогу удобно отслеживать привычки и напоминать о них.\n"
        f"Но для начала нужно пройти регистрацию, чтобы мной можно было пользоваться"
        f"на любом аккаунте в телеграм",
    )


def register_help(bot: TeleBot) -> None:
    bot.register_message_handler(
        start,
        commands=["start"],
    )
