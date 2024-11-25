from telebot import TeleBot

from frontend.loader import bot
from telebot.types import Message


@bot.message_handler(commands=["start"])
def start(message: Message):
    bot.send_message(
        message.chat.id,
        f"Привет, {message.from_user.first_name}!\n"
    )


def register_help(bot: TeleBot) -> None:
    bot.register_message_handler(
        start,
        commands=["start"],
    )
