from inline.callback.enums import HabitPropertiesEnum
from inline.callback.factories import opportunities_for_change_factory
from states.habits import ChangeHabitStates
from telebot import TeleBot
from telebot.types import CallbackQuery, Message
from utils.cache_keys import CONTEXT_KEY, HABITS_KEY
from utils.router_assistants.update_habit import (
    change_property_by_message,
    request_new_property,
)


def request_new_name(callback: CallbackQuery, bot: TeleBot) -> None:
    """
    Запрашивает новое название привычки
    :param callback: CallbackQuery
    :param bot: TeleBot
    """
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


def change_name(message: Message, bot: TeleBot) -> None:
    """
    Меняет название привычки на бэкэнде
    :param message: Message
    :param bot: TeleBot
    """
    change_property_by_message(message=message, bot=bot, key="name")


def register_change_name(bot: TeleBot) -> None:
    """
    Регистрирует request_new_name, change_name
    :param bot:
    :return:
    """
    bot.register_callback_query_handler(
        request_new_name,
        pass_bot=True,
        func=None,
        config=opportunities_for_change_factory.filter(
            property=str(HabitPropertiesEnum.NAME)
        ),
    )
    bot.register_message_handler(
        change_name, pass_bot=True, state=ChangeHabitStates.name
    )
