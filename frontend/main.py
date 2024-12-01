import logging

from telebot.custom_filters import StateFilter

from handlers.auth.register import register_auth_user
from handlers.default.cancel import register_cancel
from loader import bot
from handlers.default.start import register_help
from middlewares.logging import LoggingMiddleware

if __name__ == "__main__":
    logger = logging.getLogger(__name__)
    logging.basicConfig(
        level=logging.INFO,
        format="%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s",
    )
    logger.info("start bot")
    bot.add_custom_filter(StateFilter(bot))
    bot.setup_middleware(LoggingMiddleware())
    register_help(bot)
    register_auth_user(bot)
    register_cancel(bot)
    bot.polling()
