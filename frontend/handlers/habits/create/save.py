from telebot import TeleBot
from telebot.types import Message, CallbackQuery

from api.habits.create_habit import create_new_habit
from api.users.get_token import get_new_access_token_by_id
from states.habits import HabitsStates
from utils.constants import NAME_KEY, COUNT_KEY, HOUR_KEY, TOKEN_KEY

from utils.refresh_token import get_response_and_refresh_token


def save_habit_with_description(message: Message, bot: TeleBot):
    with bot.retrieve_data(message.chat.id, message.chat.id) as data:
        print("d", data)
        name = data[NAME_KEY]
        count = data[COUNT_KEY]
        hour = data[HOUR_KEY]
        token = data[TOKEN_KEY]
    result = get_response_and_refresh_token(
        telegram_id=message.chat.id,
        func=create_new_habit,
        access_token=token,
        name=name,
        count=count,
        hour=hour,
        description=message.text,
    )
    if result:
        bot.send_message(message.chat.id, "Привычка успешно добавлена!")
    else:
        bot.send_message(message.chat.id, "Что-то пошло не так, попробуйте позже.")
    bot.delete_state(user_id=message.chat.id)


def save_habit_without_description(callback: CallbackQuery, bot: TeleBot):
    with bot.retrieve_data(callback.from_user.id, callback.from_user.id) as data:
        name = data[NAME_KEY]
        count = data[COUNT_KEY]
        hour = data[HOUR_KEY]
        token = data[TOKEN_KEY]

    result = get_response_and_refresh_token(
        telegram_id=callback.from_user.id,
        func=create_new_habit,
        access_token=token,
        name=name,
        count=count,
        hour=hour,
        description="Пока нет описания",
    )
    if result:
        bot.edit_message_text(
            message_id=callback.message.id,
            chat_id=callback.message.chat.id,
            text="Привычка успешно добавлена!",
        )
    else:
        bot.edit_message_text(
            message_id=callback.message.id,
            chat_id=callback.message.chat.id,
            text="Что-то пошло не так, попробуйте позже.",
        )
    print("c", callback.from_user.id)
    bot.delete_state(user_id=callback.from_user.id)


def register_save_habit(bot: TeleBot):
    bot.register_message_handler(
        save_habit_with_description, pass_bot=True, state=HabitsStates.save
    )
    bot.register_callback_query_handler(
        save_habit_without_description,
        pass_bot=True,
        func=lambda c: True,
        state=HabitsStates.save,
    )
