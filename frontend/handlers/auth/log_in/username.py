from inline.callback.callbacks import LOG_IN_CALLBACK
from states.auth import LogInStates
from telebot import TeleBot
from telebot.types import CallbackQuery
from utils.router_assistants.auth import ask_for_username


def log_in_to_another_account(callback: CallbackQuery, bot: TeleBot):
    ask_for_username(
        callback=callback,
        bot=bot,
        state=LogInStates.username,
    )


def register_log_in_username(bot: TeleBot):
    bot.register_callback_query_handler(
        log_in_to_another_account,
        pass_bot=True,
        func=lambda clb: clb.data == LOG_IN_CALLBACK,
    )
