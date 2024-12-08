from telebot.types import Message, CallbackQuery

from keyboards.inline.keypads.habits import (
    get_actions_with_habit_kb,
    get_actions_with_completed_habit_kb,
)
from utils.constants import COMPLETED_KEY
from utils.output import get_habit_details_from_cache

from telebot import TeleBot

from states.habits import ReadHabitStates


def get_habit_details_by_text(message: Message, bot: TeleBot):
    number = int(message.text)
    with bot.retrieve_data(message.chat.id, message.chat.id) as data:
        text = get_habit_details_from_cache(data=data, number=number)
        is_complete_null = data[COMPLETED_KEY]
    if text is None:
        bot.send_message(
            message.chat.id, "Не нашлось номера с такой привычкой, попробуйте снова"
        )
        return
    reply_markup = (
        get_actions_with_habit_kb(number)
        if is_complete_null
        else get_actions_with_completed_habit_kb(number)
    )
    bot.send_message(message.chat.id, text, reply_markup=reply_markup)


def get_habit_details_by_callback(callback: CallbackQuery, bot: TeleBot):
    number = int(callback.data)
    with bot.retrieve_data(callback.from_user.id, callback.from_user.id) as data:
        text = get_habit_details_from_cache(data=data, number=number)
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


def register_get_habit_details(bot: TeleBot):
    bot.register_message_handler(
        get_habit_details_by_text,
        regexp=r"\d+",
        state=ReadHabitStates.details,
        pass_bot=True,
    )
    bot.register_callback_query_handler(
        get_habit_details_by_callback,
        state=ReadHabitStates.details,
        func=lambda c: c.data.isdigit(),
        pass_bot=True,
    )
