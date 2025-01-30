from database.crud.check_user import get_user_token
from inline.keypads.cancel import get_cancel_kb
from telebot import State, TeleBot
from telebot.types import CallbackQuery


def ask_for_username(callback: CallbackQuery, bot: TeleBot, state: State) -> None:
    """
    Запрашивает имя пользователя.
    Если пользователь нажал на кнопку после регистрации выводит информацию об ошибке.
    Если пользователя нет в базе, устанавливает новое состояние и просит ввести имя
    :param callback: CallbackQuery
    :param bot: TeleBot
    :param state: State
    """
    token = get_user_token(telegram_id=callback.from_user.id)
    if token is not None:
        bot.answer_callback_query(
            callback_query_id=callback.id,
            text="Вы уже зарегистрированы",
            show_alert=True,
        )
        bot.delete_message(
            chat_id=callback.from_user.id, message_id=callback.message.id
        )
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
