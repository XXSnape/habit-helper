from inline.callback.enums import HabitPropertiesEnum
from inline.callback.factories import opportunities_for_change_factory
from states.habits import ChangeHabitStates
from telebot import TeleBot
from telebot.types import CallbackQuery, Message
from utils.cache_keys import CONTEXT_KEY, HABITS_KEY
from utils.router_assistants.update_habit import (change_property_by_message,
                                                  request_new_property)


def request_new_description(callback: CallbackQuery, bot: TeleBot) -> None:
    """
    Запрашивает новое описание для привычки для обновления
    :param callback: CallbackQuery
    :param bot: TeleBot
    """
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


def change_description(message: Message, bot: TeleBot) -> None:
    """
    Меняет описание привычки на бэкэнде
    :param message: Message
    :param bot: TeleBot
    """
    change_property_by_message(message=message, bot=bot, key="description")


def register_change_description(bot: TeleBot) -> None:
    """
    Регистрирует request_new_description, change_description
    :param bot: TeleBot
    """
    bot.register_callback_query_handler(
        request_new_description,
        pass_bot=True,
        func=None,
        config=opportunities_for_change_factory.filter(
            property=str(HabitPropertiesEnum.DESCRIPTION)
        ),
    )
    bot.register_message_handler(
        change_description, pass_bot=True, state=ChangeHabitStates.description
    )
