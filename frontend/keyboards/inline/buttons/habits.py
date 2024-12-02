from enum import StrEnum

from telebot.callback_data import CallbackData

from keyboards.inline.callback.callbacks import MY_HABITS_CALLBACK, CB
from keyboards.inline.callback.constants import (
    MY_HABITS_OUTPUT,
    EDIT_HABIT_OUTPUT,
    NAME_OUTPUT,
    HOUR_OUTPUT,
    COUNT_OUTPUT,
    DESCRIPTION_OUTPUT,
    IS_FROZEN_OUTPUT,
)


class HabitProperties(StrEnum):
    NAME = "name"
    HOUR = "hour"
    COUNT = "count"
    DESCRIPTION = "description"
    IS_FROZEN = "is_frozen"


edit_habits_factory = CallbackData("num_habit", prefix="edit_habit")
opportunities_for_change_factory = CallbackData("num_habit", "property", prefix="edit")


def get_my_habits_btn() -> dict[str, dict[str, str]]:
    return {MY_HABITS_OUTPUT: {CB: MY_HABITS_CALLBACK}}


def get_selection_to_edit_btn(number: str) -> dict[str, dict[str, str]]:
    return {EDIT_HABIT_OUTPUT: {CB: edit_habits_factory.new(num_habit=number)}}


def get_habit_properties_buttons(number: str):
    return {
        NAME_OUTPUT: {
            CB: opportunities_for_change_factory.new(
                num_habit=number, property=HabitProperties.NAME
            )
        },
        HOUR_OUTPUT: {
            CB: opportunities_for_change_factory.new(
                num_habit=number, property=HabitProperties.HOUR
            )
        },
        COUNT_OUTPUT: {
            CB: opportunities_for_change_factory.new(
                num_habit=number, property=HabitProperties.COUNT
            )
        },
        DESCRIPTION_OUTPUT: {
            CB: opportunities_for_change_factory.new(
                num_habit=number, property=HabitProperties.DESCRIPTION
            )
        },
        IS_FROZEN_OUTPUT: {
            CB: opportunities_for_change_factory.new(
                num_habit=number, property=HabitProperties.IS_FROZEN
            )
        },
    }
