from telebot import TeleBot
from telebot.types import CallbackQuery

from keyboards.inline.callback.callbacks import CALL_OFF_CALLBACK


def cancel(callback: CallbackQuery, bot: TeleBot):
    bot.delete_state(user_id=callback.from_user.id)
    bot.edit_message_text(
        text="Состояние успешно сброшено!",
        message_id=callback.message.id,
        chat_id=callback.message.chat.id,
    )


def register_cancel(bot: TeleBot):
    bot.register_callback_query_handler(
        cancel, pass_bot=True, func=lambda clb: clb.data == CALL_OFF_CALLBACK
    )
