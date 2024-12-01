from telebot import TeleBot


def get_my_habits():
    pass


def register_get_habits(bot: TeleBot):
    bot.register_message_handler(get_my_habits)
