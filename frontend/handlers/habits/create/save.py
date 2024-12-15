from telebot import TeleBot
from telebot.types import Message, CallbackQuery

from api.habits.create_habit import create_new_habit
from states.habits import CreateHabitStates
from utils.cache_keys import NAME_KEY, COUNT_KEY, HOUR_KEY, TOKEN_KEY

from utils.refresh_token import get_response_and_refresh_token
from utils.texts import COMMANDS, HABIT_WAS_CREATED


def save_habit_with_description(message: Message, bot: TeleBot):
    with bot.retrieve_data(message.chat.id, message.chat.id) as data:
        name = data[NAME_KEY]
        count = data[COUNT_KEY]
        hour = data[HOUR_KEY]
        token = data[TOKEN_KEY]
    get_response_and_refresh_token(
        telegram_id=message.chat.id,
        func=create_new_habit,
        access_token=token,
        name=name,
        count=count,
        hour=hour,
        description=message.text,
    )
    bot.delete_state(user_id=message.chat.id, chat_id=message.chat.id)
    bot.send_message(message.chat.id, text=HABIT_WAS_CREATED)
    bot.send_message(message.chat.id, text=COMMANDS)


def save_habit_without_description(callback: CallbackQuery, bot: TeleBot):
    with bot.retrieve_data(callback.from_user.id, callback.from_user.id) as data:
        name = data[NAME_KEY]
        count = data[COUNT_KEY]
        hour = data[HOUR_KEY]
        token = data[TOKEN_KEY]

    get_response_and_refresh_token(
        telegram_id=callback.from_user.id,
        func=create_new_habit,
        access_token=token,
        name=name,
        count=count,
        hour=hour,
        description="Пока нет описания",
    )
    bot.delete_state(user_id=callback.from_user.id, chat_id=callback.from_user.id)
    bot.edit_message_text(
        message_id=callback.message.id,
        chat_id=callback.message.chat.id,
        text=HABIT_WAS_CREATED,
    )
    bot.send_message(callback.message.id, text=COMMANDS)


def register_save_habit(bot: TeleBot):
    bot.register_message_handler(
        save_habit_with_description, pass_bot=True, state=CreateHabitStates.save
    )
    bot.register_callback_query_handler(
        save_habit_without_description,
        pass_bot=True,
        func=lambda c: True,
        state=CreateHabitStates.save,
    )
