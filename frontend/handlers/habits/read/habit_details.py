from inline.callback.constants import MENU_OUTPUT
from inline.callback.factories import habit_details_factory
from inline.keypads.cancel import get_cancel_kb
from inline.keypads.habits import (get_actions_with_completed_habit_kb,
                                   get_actions_with_habit_kb)
from states.habits import ReadHabitStates
from telebot import TeleBot
from telebot.types import CallbackQuery, Message
from utils.cache_keys import COMPLETED_KEY
from utils.output import get_habit_details_from_cache


def get_habit_details_by_text(message: Message, bot: TeleBot) -> None:
    """
    Выводит информацию о деталях привычке после ввода её номера в кэше
    :param message: Message
    :param bot: TeleBot
    """
    number = int(message.text)
    with bot.retrieve_data(message.chat.id, message.chat.id) as data:
        text = get_habit_details_from_cache(cache=data, number=number)
        is_complete_null = data[COMPLETED_KEY]
    if text is None:
        bot.send_message(
            message.chat.id,
            "Не нашлось номера с такой привычкой, попробуйте снова",
            reply_markup=get_cancel_kb(MENU_OUTPUT),
        )
        return
    reply_markup = (
        get_actions_with_habit_kb(number)
        if is_complete_null
        else get_actions_with_completed_habit_kb(number)
    )
    bot.send_message(message.chat.id, text, reply_markup=reply_markup)


def get_habit_details_by_callback(callback: CallbackQuery, bot: TeleBot) -> None:
    """
    Выводит информацию о деталях привычки после нажатия на кнопку с данными о её номере в кэше
    :param callback: CallbackQuery
    :param bot: TeleBot
    """
    number = int(habit_details_factory.parse(callback.data)["num_habit"])
    with bot.retrieve_data(callback.from_user.id, callback.from_user.id) as data:
        text = get_habit_details_from_cache(cache=data, number=number)
        is_complete_null = data[COMPLETED_KEY]
    reply_markup = (
        get_actions_with_habit_kb(number)
        if is_complete_null
        else get_actions_with_completed_habit_kb(number)
    )
    bot.edit_message_text(
        message_id=callback.message.id,
        chat_id=callback.message.chat.id,
        text=text,
        reply_markup=reply_markup,
    )


def register_get_habit_details(bot: TeleBot) -> None:
    """
    Регистрирует get_habit_details_by_text, get_habit_details_by_callback
    :param bot:
    :return:
    """
    bot.register_message_handler(
        get_habit_details_by_text,
        regexp=r"\d+",
        state=ReadHabitStates.details,
        pass_bot=True,
    )
    bot.register_callback_query_handler(
        get_habit_details_by_callback,
        func=None,
        config=habit_details_factory.filter(),
        pass_bot=True,
    )
