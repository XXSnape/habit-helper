import logging

from apscheduler.schedulers.background import BackgroundScheduler
from telebot import TeleBot
from telebot.custom_filters import StateFilter

import handlers.auth as auth
import handlers.habits as habits
from handlers.default.cancel import register_cancel
from handlers.default.unrecognized import register_unrecognized_message
from keyboards.inline.filters.habits import EditHabitCallbackFilter
from loader import bot
from handlers.default.start import register_help
from middlewares.logging import LoggingMiddleware
from utils.scheduler.settings import register_tasks


def register_handlers(bot: TeleBot):
    register_cancel(bot)
    register_help(bot)
    auth.register_username(bot)
    auth.register_password(bot)
    auth.register_saving_user(bot)
    auth.register_log_in_username(bot)
    auth.register_log_in_password(bot)
    auth.register_log_in(bot)
    habits.register_get_name(bot)
    habits.register_get_count(bot)
    habits.register_get_hour(bot)
    habits.register_get_description(bot)
    habits.register_save_habit(bot)
    habits.register_mark_habit(bot)
    habits.register_get_habits(bot)
    habits.register_get_habit_details(bot)
    habits.register_provide_with_choosing(bot)
    habits.register_delete_habit(bot)
    habits.register_change_name(bot)
    habits.register_change_time(bot)
    habits.register_change_frozen(bot)
    habits.register_change_count(bot)
    habits.register_change_description(bot)
    habits.register_calendar(bot)

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
    bot.add_custom_filter(EditHabitCallbackFilter())
    register_handlers(bot)
    # scheduler = BackgroundScheduler()
    # scheduler.configure(timezone="Europe/Moscow")
    # register_tasks(scheduler=scheduler, bot=bot)
    # scheduler.start()
    bot.polling()
