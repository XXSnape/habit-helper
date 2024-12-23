from inline.callback.callbacks import (
    MY_HABITS_CALLBACK,
    CB,
    REJECTION_REASON_CALLBACK,
)
from inline.callback.constants import (
    MY_HABITS_OUTPUT,
    EDIT_HABIT_OUTPUT,
    NAME_OUTPUT,
    HOUR_OUTPUT,
    COUNT_OUTPUT,
    DESCRIPTION_OUTPUT,
    IS_FROZEN_OUTPUT,
    DELETE_HABIT_OUTPUT,
    IS_UNFROZEN_OUTPUT,
    STATISTIC_OUTPUT,
    HABIT_COMPLETED_OUTPUT,
    HABIT_NOT_COMPLETED_OUTPUT,
    REJECTION_REASON_OUTPUT,
    RESUME_OUTPUT,
    BACK_OUTPUT,
)
from inline.callback.enums import HabitPropertiesEnum, ActionsHabitEnum
from inline.callback.factories import (
    actions_with_habit_factory,
    opportunities_for_change_factory,
    mark_habit_factory,
    habit_details_factory,
    freeze_habit_factory,
)
from .types import Buttons


def get_my_habits_btn() -> Buttons:
    """
    Возвращает кнопку для получения привычек пользователя
    :return: Buttons
    """
    return {MY_HABITS_OUTPUT: {CB: MY_HABITS_CALLBACK}}


def get_tagging_buttons(habit_id: int, date: str) -> Buttons:
    """
    Возвращает кнопки для пометки, выполнена задача или нет,
    а также для того, чтобы приостановить привычку
    :param habit_id: id привычки на бэкэнде
    :param date: дата, за которую нужно отметить выполнение
    :return: Buttons
    """
    return {
        HABIT_COMPLETED_OUTPUT: {
            CB: mark_habit_factory.new(habit_id=habit_id, date=date, is_done="1")
        },
        HABIT_NOT_COMPLETED_OUTPUT: {
            CB: mark_habit_factory.new(habit_id=habit_id, date=date, is_done="0")
        },
        IS_FROZEN_OUTPUT: {CB: freeze_habit_factory.new(habit_id=habit_id)},
    }


def get_reason_waiver_btn() -> Buttons:
    """
    Возвращает кнопку, чтобы не указывать причину невыполнения задачи
    :return: Buttons
    """
    return {REJECTION_REASON_OUTPUT: {CB: REJECTION_REASON_CALLBACK}}


def get_habit_details_btn(number: int) -> Buttons:
    """
    Возвращает кнопку для возврата к деталям привычки
    :param number: номер привычки в кэше
    :return: Buttons
    """
    return {BACK_OUTPUT: {CB: habit_details_factory.new(num_habit=number)}}


def get_selection_to_edit_btn(number: int, key: str = EDIT_HABIT_OUTPUT) -> Buttons:
    """
    Возвращает кнопку для возможности редактировать параметры привычки
    :param number: номер привычки в кэше
    :param key: надпись на кнопке
    :return: Buttons
    """
    return {
        key: {
            CB: actions_with_habit_factory.new(
                num_habit=number, action=ActionsHabitEnum.EDIT
            )
        }
    }


def get_statistics_btn(number: int) -> Buttons:
    """
    Возвращает кнопку для просмотра статистики выполнений ежедневного задания
    :param number: номер привычки в кэше
    :return: Buttons
    """
    return {
        STATISTIC_OUTPUT: {
            CB: actions_with_habit_factory.new(
                num_habit=number, action=ActionsHabitEnum.VIEW
            )
        }
    }


def get_resuming_btn(number: int) -> Buttons:
    """
    Возвращает кнопку для возобновления приостановленной привычки
    :param number: номер привычки в кэше
    :return: Buttons
    """
    return {
        RESUME_OUTPUT: {
            CB: actions_with_habit_factory.new(
                num_habit=number, action=ActionsHabitEnum.RESUME
            )
        }
    }


def get_deleting_habit_btn(number: int) -> Buttons:
    """
    Возвращает кнопку для удаления привычки
    :param number: номер в кэше
    :return: Buttons
    """
    return {
        DELETE_HABIT_OUTPUT: {
            CB: actions_with_habit_factory.new(
                num_habit=number, action=ActionsHabitEnum.DELETE
            )
        }
    }


def get_habit_properties_buttons(number: int, iz_frozen: bool) -> Buttons:
    """
    Возвращает кнопки с параметрами привычек для редактирования
    :param number: номер в кэше
    :param iz_frozen: приостановлена привычка или нет
    :return: Buttons
    """
    values = {
        NAME_OUTPUT: {
            CB: opportunities_for_change_factory.new(
                num_habit=number, property=HabitPropertiesEnum.NAME
            )
        },
        HOUR_OUTPUT: {
            CB: opportunities_for_change_factory.new(
                num_habit=number, property=HabitPropertiesEnum.HOUR
            )
        },
        COUNT_OUTPUT: {
            CB: opportunities_for_change_factory.new(
                num_habit=number, property=HabitPropertiesEnum.COUNT
            )
        },
        DESCRIPTION_OUTPUT: {
            CB: opportunities_for_change_factory.new(
                num_habit=number, property=HabitPropertiesEnum.DESCRIPTION
            )
        },
    }
    data = {
        CB: opportunities_for_change_factory.new(
            num_habit=number, property=HabitPropertiesEnum.IS_FROZEN
        )
    }
    if iz_frozen is False:
        values[IS_FROZEN_OUTPUT] = data
    else:
        values[IS_UNFROZEN_OUTPUT] = data
    return values
