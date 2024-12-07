from telebot import TeleBot
from telebot.types import CallbackQuery

from keyboards.inline.callback.callbacks import REGISTRATION_CALLBACK
from keyboards.inline.keypads.cancel import get_cancel_kb
from states.auth import AuthStates


def request_username(callback: CallbackQuery, bot: TeleBot):
    bot.set_state(
        user_id=callback.from_user.id,
        chat_id=callback.message.chat.id,
        state=AuthStates.username,
    )
    bot.edit_message_text(
        message_id=callback.message.id,
        chat_id=callback.message.chat.id,
        text=f"Пожалуйста, введите никнейм для использования бота.",
        reply_markup=get_cancel_kb(),
    )


def register_username(bot: TeleBot):
    bot.register_callback_query_handler(
        request_username,
        pass_bot=True,
        func=lambda clb: clb.data == REGISTRATION_CALLBACK,
    )
