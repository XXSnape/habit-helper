from telebot import TeleBot
from telebot.types import Message


def unrecognized_message(message: Message, bot: TeleBot):
    bot.send_message(
        message.chat.id,
        "Доступные команды:\n\n" "/start\n" "/create_habit\n" "/my_habits\n /log_in",
    )


def register_unrecognized_message(bot: TeleBot):
    bot.register_message_handler(unrecognized_message, pass_bot=True)
