from telebot import TeleBot
from telebot.types import CallbackQuery

from inline.callback.callbacks import CALL_OFF_CALLBACK
from utils.texts import COMMANDS


def cancel_and_get_menu(callback: CallbackQuery, bot: TeleBot):
    bot.delete_state(user_id=callback.from_user.id)
    bot.edit_message_text(
        text=COMMANDS,
        message_id=callback.message.id,
        chat_id=callback.message.chat.id,
    )


def register_cancel(bot: TeleBot):
    bot.register_callback_query_handler(
        cancel_and_get_menu,
        pass_bot=True,
        func=lambda clb: clb.data == CALL_OFF_CALLBACK,
    )
