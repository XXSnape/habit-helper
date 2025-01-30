from inline.callback.callbacks import CALL_OFF_CALLBACK
from telebot import TeleBot
from telebot.custom_filters import TextFilter
from telebot.types import CallbackQuery
from utils.texts import COMMANDS


def cancel_and_get_menu(callback: CallbackQuery, bot: TeleBot) -> None:
    """
    Обрабатывает нажатие на кнопку отмены действия.
    Сбрасывает состояние и выводит возможности бота

    :param callback: CallbackQuery
    :param bot: TeleBot

    """
    bot.delete_state(user_id=callback.from_user.id)
    bot.edit_message_text(
        text=COMMANDS,
        message_id=callback.message.id,
        chat_id=callback.message.chat.id,
    )


def register_cancel(bot: TeleBot) -> None:
    """
    Регистрирует cancel_and_get_menu
    :param bot: TeleBot
    """
    bot.register_callback_query_handler(
        cancel_and_get_menu,
        pass_bot=True,
        text=TextFilter(equals=CALL_OFF_CALLBACK),
        func=None,
    )
