from telebot import TeleBot
from telebot.types import Message

from keyboards.inline.keypads.time import get_hour_selection_kb
from states.habits import CreateHabitStates
from utils.constants import COUNT_KEY


def request_hour(message: Message, bot: TeleBot):
    with bot.retrieve_data(message.chat.id, message.chat.id) as data:
        data[COUNT_KEY] = int(message.text)
    bot.send_message(
        message.chat.id,
        "Выберете удобное время по Москве, в которое отправлять напоминание",
        reply_markup=get_hour_selection_kb(),
    )
    bot.set_state(
        user_id=message.chat.id, chat_id=message.chat.id, state=CreateHabitStates.hour
    )


def register_get_hour(bot: TeleBot):
    bot.register_message_handler(
        request_hour, pass_bot=True, state=CreateHabitStates.count
    )
