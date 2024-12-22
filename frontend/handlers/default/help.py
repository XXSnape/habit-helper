from telebot import TeleBot

from telebot.types import Message

from utils.texts import ABOUT_BOT


def help(message: Message, bot: TeleBot):
    bot.send_message(message.chat.id, text=ABOUT_BOT)


def register_help(bot: TeleBot) -> None:
    bot.register_message_handler(help, commands=["help"], pass_bot=True)
