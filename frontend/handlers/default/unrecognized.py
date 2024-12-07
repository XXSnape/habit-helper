from telebot import TeleBot
from telebot.types import Message

from utils.mailing import send_reminders_to_all_users


def unrecognized_message(message: Message, bot: TeleBot):
    bot.send_message(
        message.chat.id,
        "Доступные команды:\n\n" "/start\n" "/create_habit\n" "/my_habits",
    )
    send_reminders_to_all_users(bot, 7)


def register_unrecognized_message(bot: TeleBot):
    bot.register_message_handler(unrecognized_message, pass_bot=True)
