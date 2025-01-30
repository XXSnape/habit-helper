from inline.callback.enums import HabitPropertiesEnum
from inline.callback.factories import opportunities_for_change_factory
from inline.keypads.time import get_hour_selection_and_back_kb
from states.habits import ChangeHabitStates
from telebot import TeleBot
from telebot.types import CallbackQuery
from utils.cache_keys import CONTEXT_KEY, HABITS_KEY
from utils.output import get_format_hour
from utils.router_assistants.update_habit import (change_property_by_callback,
                                                  request_new_property)


def request_new_time(callback: CallbackQuery, bot: TeleBot) -> None:
    """
    Запрашивает новое время для уведомления
    :param callback: CallbackQuery
    :param bot: TeleBot
    """
    number = int(opportunities_for_change_factory.parse(callback.data)["num_habit"])
    with bot.retrieve_data(callback.from_user.id, callback.from_user.id) as data:
        last_time = get_format_hour(data[HABITS_KEY][number]["notification_hour"])
        data[CONTEXT_KEY] = number

    request_new_property(
        callback=callback,
        bot=bot,
        new_state=ChangeHabitStates.hour,
        message=f"Выберете другое время, вместо {last_time}",
        number=number,
        reply_markup=get_hour_selection_and_back_kb,
    )


def change_time(callback: CallbackQuery, bot: TeleBot) -> None:
    """
    Обновляет время напоминания привычки на бэкэнде
    :param callback: CallbackQuery
    :param bot: TeleBot
    """
    with bot.retrieve_data(callback.from_user.id, callback.from_user.id) as data:
        change_property_by_callback(
            callback=callback,
            bot=bot,
            message="Привычка успешно обновлена!",
            new_data={"notification_hour": int(callback.data)},
            cache=data,
            number=data[CONTEXT_KEY],
        )


def register_change_time(bot: TeleBot) -> None:
    """
    Регистрирует request_new_time, change_time
    :param bot: TeleBot
    """
    bot.register_callback_query_handler(
        request_new_time,
        pass_bot=True,
        func=None,
        config=opportunities_for_change_factory.filter(
            property=str(HabitPropertiesEnum.HOUR)
        ),
    )
    bot.register_callback_query_handler(
        change_time, pass_bot=True, func=None, state=ChangeHabitStates.hour
    )
