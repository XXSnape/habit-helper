from api.habits.update_habit import update_habit
from inline.keypads.habits import get_actions_with_habit_kb, get_back_to_action_kb
from states.habits import ReadHabitStates
from telebot import State, TeleBot
from telebot.types import CallbackQuery, Message
from utils.cache_keys import CONTEXT_KEY, TOKEN_KEY
from utils.refresh_token import get_response_and_refresh_token


def request_new_property(
    callback: CallbackQuery,
    bot: TeleBot,
    new_state: State,
    message: str,
    number: int,
    reply_markup=get_back_to_action_kb,
) -> None:
    """
    Запрашивает значение нового параметра у привычки.
    Устанавливает новое состояние и редактирует сообщение
    с просьбой предоставить новое значение

    :param callback: CallbackQuery
    :param bot: TeleBot
    :param new_state: State
    :param message: сообщение пользователю
    :param number: номер привычки в кэше
    :param reply_markup: клавиатура для пользователя
    :return:
    """
    bot.set_state(
        user_id=callback.from_user.id,
        chat_id=callback.from_user.id,
        state=new_state,
    )
    bot.edit_message_text(
        message_id=callback.message.id,
        chat_id=callback.message.chat.id,
        text=message,
        reply_markup=reply_markup(number),
    )


def change_property_by_message(
    message: Message, bot: TeleBot, key: str, is_integer: bool = False
) -> None:
    """
    Делает запрос на изменение параметра привычки.
    Новое значение берет из поступившего сообщения
    :param message: Message
    :param bot: TeleBot
    :param key: ключ для отправки данных на бэкэнд
    :param is_integer: являются ли отправляемые данные числом или нет
    """
    with bot.retrieve_data(message.chat.id, message.chat.id) as data:
        number = data[CONTEXT_KEY]
        text = get_response_and_refresh_token(
            telegram_id=message.chat.id,
            func=update_habit,
            access_token=data[TOKEN_KEY],
            number=number,
            new_data={key: int(message.text) if is_integer else message.text},
            cache=data,
        )
    bot.set_state(
        chat_id=message.chat.id, user_id=message.chat.id, state=ReadHabitStates.details
    )
    bot.send_message(
        message.chat.id, text=text, reply_markup=get_actions_with_habit_kb(number)
    )


def change_property_by_callback(
    callback: CallbackQuery,
    bot: TeleBot,
    message: str,
    new_data: dict,
    cache: dict,
    number: int,
) -> None:
    """
    Делает запрос на изменение параметра привычки после нажатия на кнопку

    :param callback: CallbackQuery
    :param bot: TeleBot
    :param message: сообщение для пользователя
    :param new_data: обновленные данные у привычки
    :param cache: кэш с данными
    :param number: номер привычки в кэше
    """

    text = get_response_and_refresh_token(
        telegram_id=callback.from_user.id,
        func=update_habit,
        access_token=cache[TOKEN_KEY],
        number=number,
        new_data=new_data,
        cache=cache,
    )
    bot.edit_message_text(
        message_id=callback.message.id,
        chat_id=callback.message.chat.id,
        text=text,
        reply_markup=get_actions_with_habit_kb(number),
    )
    bot.answer_callback_query(
        callback_query_id=callback.id,
        text=message,
        show_alert=True,
    )
    bot.set_state(
        chat_id=callback.from_user.id,
        user_id=callback.from_user.id,
        state=ReadHabitStates.details,
    )
