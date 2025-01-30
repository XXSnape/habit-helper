from inline.callback.callbacks import REGISTRATION_CALLBACK
from states.auth import AuthStates
from telebot import TeleBot
from telebot.custom_filters import TextFilter
from telebot.types import CallbackQuery
from utils.router_assistants.auth import ask_for_username


def request_username(callback: CallbackQuery, bot: TeleBot) -> None:
    """
    Запрашивает имя пользователя для регистрации
    :param callback: CallbackQuery
    :param bot: TeleBot
    """
    ask_for_username(
        callback=callback,
        bot=bot,
        state=AuthStates.username,
    )


def register_username(bot: TeleBot) -> None:
    """
    Регистрирует request_username
    :param bot: TeleBot
    """
    bot.register_callback_query_handler(
        request_username,
        pass_bot=True,
        text=TextFilter(equals=REGISTRATION_CALLBACK),
        func=None,
    )
