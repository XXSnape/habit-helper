from telebot import TeleBot
from telebot.types import Message

from inline.keypads.time import get_hour_selection_kb
from states.habits import CreateHabitStates
from utils.cache_keys import COUNT_KEY


def request_hour(message: Message, bot: TeleBot) -> None:
    """
    Запрашивает час для отправки
    :param message: Message
    :param bot: TeleBot
    """
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


def register_get_hour(bot: TeleBot) -> None:
    """
    Регистрирует request_hour
    :param bot: TeleBot
    """
    bot.register_message_handler(
        request_hour, pass_bot=True, state=CreateHabitStates.count
    )
