from telebot import TeleBot
from telebot.types import Message, CallbackQuery

from keyboards.inline.callback.callbacks import MY_HABITS_CALLBACK
from states.habits import ReadHabitStates
from utils.constants import TEXT_KEY
from utils.refresh_token import get_response_and_refresh_token

from api.habits.my_habits import get_my_habits_by_token
from handlers.default.registration_error import check_registration


def get_my_habits_by_command(message: Message, bot: TeleBot):
    bot.set_state(
        user_id=message.chat.id,
        chat_id=message.chat.id,
        state=ReadHabitStates.details,
    )
    token = check_registration(message.chat.id, bot)
    if token is None:
        return
    with bot.retrieve_data(message.chat.id, message.chat.id) as data:
        text = get_response_and_refresh_token(
            telegram_id=message.chat.id,
            func=get_my_habits_by_token,
            access_token=token,
            data=data,
        )
    if text is None:
        bot.send_message(message.chat.id, "Нет ни одной привычки.")
        return
    bot.send_message(message.chat.id, text)


def get_my_habits_by_callback(callback: CallbackQuery, bot: TeleBot):
    with bot.retrieve_data(callback.from_user.id, callback.from_user.id) as data:
        text = data[TEXT_KEY]
    bot.edit_message_text(
        message_id=callback.message.id, chat_id=callback.message.chat.id, text=text
    )


def register_get_habits(bot: TeleBot):
    bot.register_message_handler(
        get_my_habits_by_command, pass_bot=True, commands=["my_habits"]
    )
    bot.register_callback_query_handler(
        get_my_habits_by_callback,
        pass_bot=True,
        func=lambda c: c.data == MY_HABITS_CALLBACK,
        state=ReadHabitStates.details,
    )
