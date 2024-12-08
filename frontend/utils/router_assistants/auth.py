from telebot import State, TeleBot
from telebot.types import CallbackQuery

from keyboards.inline.keypads.cancel import get_cancel_kb


def ask_for_username(callback: CallbackQuery, bot: TeleBot, state: State):
    bot.set_state(
        user_id=callback.from_user.id,
        chat_id=callback.message.chat.id,
        state=state,
    )
    bot.edit_message_text(
        message_id=callback.message.id,
        chat_id=callback.message.chat.id,
        text="Пожалуйста, введите никнейм для использования бота.",
        reply_markup=get_cancel_kb(),
    )
