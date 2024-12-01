import logging

from telebot import TeleBot
from telebot.custom_filters import StateFilter

import handlers.auth as auth
import handlers.habits as habits

from handlers.default.cancel import register_cancel
from handlers.default.unrecognized import register_unrecognized_message
from loader import bot
from handlers.default.start import register_help
from middlewares.logging import LoggingMiddleware


def register_handlers(bot: TeleBot):
    register_cancel(bot)
    register_help(bot)
    auth.register_username(bot)
    auth.register_password(bot)
    auth.register_saving_user(bot)
    habits.register_get_name(bot)
    habits.register_get_count(bot)
    habits.register_get_hour(bot)
    habits.register_get_description(bot)
    habits.register_save_habit(bot)
    habits.register_get_habits(bot)
    register_unrecognized_message(bot)


if __name__ == "__main__":
    logger = logging.getLogger(__name__)
    logging.basicConfig(
        level=logging.INFO,
        format="%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s",
    )
    logger.info("start bot")
    bot.add_custom_filter(StateFilter(bot))
    bot.setup_middleware(LoggingMiddleware())
    register_handlers(bot)
    bot.polling()
