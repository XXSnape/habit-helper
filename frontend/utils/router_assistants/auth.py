from telebot import State, TeleBot
from telebot.types import CallbackQuery

from database.crud.check_user import get_user_token
from keyboards.inline.keypads.cancel import get_cancel_kb
from utils.delete_message import try_delete_message


def ask_for_username(callback: CallbackQuery, bot: TeleBot, state: State):
    token = get_user_token(telegram_id=callback.from_user.id)
    if token is not None:
        bot.answer_callback_query(
            callback_query_id=callback.id,
            text="Вы уже зарегистрированы",
            show_alert=True,
        )
        try_delete_message(bot=bot, callback=callback)
        return
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
