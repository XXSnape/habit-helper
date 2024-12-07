from telebot import TeleBot
from telebot.types import CallbackQuery, Message

from keyboards.inline.callback.enums import HabitProperties
from keyboards.inline.callback.factories import opportunities_for_change_factory

from states.habits import ChangeHabitStates
from utils.constants import CONTEXT_KEY, HABITS_KEY
from utils.routers_assistants import request_new_property, change_property_by_message


def request_new_name(callback: CallbackQuery, bot: TeleBot):
    number = int(opportunities_for_change_factory.parse(callback.data)["num_habit"])
    with bot.retrieve_data(callback.from_user.id, callback.from_user.id) as data:
        data[CONTEXT_KEY] = number
        old_name = data[HABITS_KEY][number]["name"]
    request_new_property(
        callback=callback,
        bot=bot,
        new_state=ChangeHabitStates.name,
        message=f"Напишите новое название для привычки «{old_name}»",
        number=number,
    )


def change_name(message: Message, bot: TeleBot):
    change_property_by_message(message=message, bot=bot, key="name")


def register_change_name(bot: TeleBot):
    bot.register_callback_query_handler(
        request_new_name,
        pass_bot=True,
        func=None,
        config=opportunities_for_change_factory.filter(
            property=str(HabitProperties.NAME)
        ),
    )
    bot.register_message_handler(
        change_name, pass_bot=True, state=ChangeHabitStates.name
    )
