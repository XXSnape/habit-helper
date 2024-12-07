from telebot import TeleBot
from telebot.types import CallbackQuery, Message


from keyboards.inline.callback.enums import HabitProperties
from keyboards.inline.callback.factories import opportunities_for_change_factory

from states.habits import ChangeHabitStates
from utils.constants import CONTEXT_KEY, HABITS_KEY
from utils.router_assistants.update_habit import (
    request_new_property,
    change_property_by_message,
)


def request_new_description(callback: CallbackQuery, bot: TeleBot):
    number = int(opportunities_for_change_factory.parse(callback.data)["num_habit"])
    with bot.retrieve_data(callback.from_user.id, callback.from_user.id) as data:
        old_name = data[HABITS_KEY][number]["name"]
        data[CONTEXT_KEY] = number
    request_new_property(
        callback=callback,
        bot=bot,
        new_state=ChangeHabitStates.description,
        message=f"Напишите новое описание для привычки «{old_name}»",
        number=number,
    )


def change_description(message: Message, bot: TeleBot):
    change_property_by_message(message=message, bot=bot, key="description")


def register_change_description(bot: TeleBot):
    bot.register_callback_query_handler(
        request_new_description,
        pass_bot=True,
        func=None,
        config=opportunities_for_change_factory.filter(
            property=str(HabitProperties.DESCRIPTION)
        ),
    )
    bot.register_message_handler(
        change_description, pass_bot=True, state=ChangeHabitStates.description
    )
