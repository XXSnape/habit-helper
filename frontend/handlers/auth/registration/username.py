from telebot import TeleBot
from telebot.types import CallbackQuery

from keyboards.inline.callback.callbacks import REGISTRATION_CALLBACK
from keyboards.inline.keypads.cancel import get_cancel_kb
from states.auth import AuthStates
from utils.router_assistants.auth import ask_for_username


def request_username(callback: CallbackQuery, bot: TeleBot):
    ask_for_username(
        callback=callback,
        bot=bot,
        state=AuthStates.username,
    )


def register_username(bot: TeleBot):
    bot.register_callback_query_handler(
        request_username,
        pass_bot=True,
        func=lambda clb: clb.data == REGISTRATION_CALLBACK,
    )
