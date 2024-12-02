from keyboards.inline.callback.callbacks import MY_HABITS_CALLBACK, CB
from keyboards.inline.callback.constants import (
    MY_HABITS_OUTPUT,
    EDIT_HABIT_OUTPUT,
    NAME_OUTPUT,
    HOUR_OUTPUT,
    COUNT_OUTPUT,
    DESCRIPTION_OUTPUT,
    IS_FROZEN_OUTPUT,
    DELETE_HABIT_OUTPUT,
)
from keyboards.inline.callback.enums import HabitProperties, ActionsHabitEnum
from keyboards.inline.callback.factories import (
    actions_with_habit_factory,
    opportunities_for_change_factory,
)


def get_my_habits_btn() -> dict[str, dict[str, str]]:
    return {MY_HABITS_OUTPUT: {CB: MY_HABITS_CALLBACK}}


def get_selection_to_edit_btn(
    number: int, key: str = EDIT_HABIT_OUTPUT
) -> dict[str, dict[str, str]]:
    return {
        key: {
            CB: actions_with_habit_factory.new(
                num_habit=number, action=ActionsHabitEnum.EDIT
            )
        }
    }


def get_deleting_habit_btn(number: int) -> dict[str, dict[str, str]]:
    return {
        DELETE_HABIT_OUTPUT: {
            CB: actions_with_habit_factory.new(
                num_habit=number, action=ActionsHabitEnum.DELETE
            )
        }
    }


def get_habit_properties_buttons(number: int):
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
