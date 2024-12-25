from telebot import TeleBot
from telebot.types import Message
from utils.texts import ABOUT_BOT


def help_command(message: Message, bot: TeleBot) -> None:
    """
    Обрабатывает команду /help
    :param message:
    :param bot:
    """
    bot.send_message(message.chat.id, text=ABOUT_BOT)


def register_help(bot: TeleBot) -> None:
    """
    Регистрирует help_command
    :param bot:
    :return:
    """
    bot.register_message_handler(help_command, commands=["help"], pass_bot=True)
