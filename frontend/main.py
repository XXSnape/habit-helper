from telebot.custom_filters import StateFilter

from loader import bot
from handlers.default.start import register_help


if __name__ == "__main__":
    bot.add_custom_filter(StateFilter(bot))
    register_help(bot)
    bot.polling()
