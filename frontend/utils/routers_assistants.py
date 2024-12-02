from telebot import TeleBot, State
from telebot.types import CallbackQuery, Message

from api.habits.update_habit import update_habit
from keyboards.inline.keypads.habits import (
    get_back_to_action_kb,
    get_actions_with_habit_kb,
)
from states.habits import ReadHabitStates
from utils.constants import CONTEXT_KEY, TOKEN_KEY
from utils.refresh_token import get_response_and_refresh_token


def request_new_property(
    callback: CallbackQuery,
    bot: TeleBot,
    new_state: State,
    message: str,
    number: int,
    reply_markup=get_back_to_action_kb,
):
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
):
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
    data: dict,
    number: int,
):

    text = get_response_and_refresh_token(
        telegram_id=callback.from_user.id,
        func=update_habit,
        access_token=data[TOKEN_KEY],
        number=number,
        new_data=new_data,
        cache=data,
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
    bot.edit_message_text(
        message_id=callback.message.id,
        chat_id=callback.message.chat.id,
        text=text,
        reply_markup=get_actions_with_habit_kb(number),
    )
