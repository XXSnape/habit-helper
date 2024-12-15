from keyboards.inline.callback.callbacks import (
    MY_HABITS_CALLBACK,
    CB,
    REJECTION_REASON_CALLBACK,
)
from keyboards.inline.callback.constants import (
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
from keyboards.inline.callback.enums import HabitProperties, ActionsHabitEnum
from keyboards.inline.callback.factories import (
    actions_with_habit_factory,
    opportunities_for_change_factory,
    mark_habit_factory,
    habit_details_factory,
    freeze_habit_factory,
)


def get_my_habits_btn() -> dict[str, dict[str, str]]:
    return {MY_HABITS_OUTPUT: {CB: MY_HABITS_CALLBACK}}


def get_tagging_buttons(habit_id: int, date: str) -> dict[str, dict[str, str]]:
    return {
        HABIT_COMPLETED_OUTPUT: {
            CB: mark_habit_factory.new(habit_id=habit_id, date=date, is_done="1")
        },
        HABIT_NOT_COMPLETED_OUTPUT: {
            CB: mark_habit_factory.new(habit_id=habit_id, date=date, is_done="0")
        },
        IS_FROZEN_OUTPUT: {CB: freeze_habit_factory.new(habit_id=habit_id)},
    }


def get_reason_waiver_btn() -> dict[str, dict[str, str]]:
    return {REJECTION_REASON_OUTPUT: {CB: REJECTION_REASON_CALLBACK}}


def get_habit_details_btn(number: int):
    return {BACK_OUTPUT: {CB: habit_details_factory.new(num_habit=number)}}


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


def get_statistics_btn(number: int) -> dict[str, dict[str, str]]:
    return {
        STATISTIC_OUTPUT: {
            CB: actions_with_habit_factory.new(
                num_habit=number, action=ActionsHabitEnum.VIEW
            )
        }
    }


def get_resuming_btn(number: int) -> dict[str, dict[str, str]]:
    return {
        RESUME_OUTPUT: {
            CB: actions_with_habit_factory.new(
                num_habit=number, action=ActionsHabitEnum.RESUME
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


def get_habit_properties_buttons(number: int, iz_frozen):
    values = {
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
    }
    data = {
        CB: opportunities_for_change_factory.new(
            num_habit=number, property=HabitProperties.IS_FROZEN
        )
    }
    if iz_frozen is False:
        values[IS_FROZEN_OUTPUT] = data
    else:
        values[IS_UNFROZEN_OUTPUT] = data
    return values
