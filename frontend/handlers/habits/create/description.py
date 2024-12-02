from telebot import TeleBot
from telebot.types import CallbackQuery

from keyboards.inline.keypads.cancel import get_refusal_to_describe_kb
from states.habits import CreateHabitStates
from utils.constants import HOUR_KEY


def request_description(callback: CallbackQuery, bot: TeleBot):
    with bot.retrieve_data(callback.message.chat.id, callback.message.chat.id) as data:
        data[HOUR_KEY] = int(callback.data)
    bot.edit_message_text(
        message_id=callback.message.id,
        chat_id=callback.message.chat.id,
        text="Введите описание, чтобы вспомнить, зачем вам данная привычка",
        reply_markup=get_refusal_to_describe_kb(),
    )
    bot.set_state(
        user_id=callback.from_user.id,
        chat_id=callback.message.chat.id,
        state=CreateHabitStates.save,
    )


def register_get_description(bot: TeleBot):
    bot.register_callback_query_handler(
        request_description,
        pass_bot=True,
        func=lambda c: True,
        state=CreateHabitStates.hour,
    )
