from telebot.types import InlineKeyboardMarkup

from keyboards.inline.buttons.habits import (
    get_my_habits_btn,
    get_selection_to_edit_btn,
    get_habit_properties_buttons,
    get_deleting_habit_btn,
    get_statistics_btn,
    get_tagging_buttons,
    get_reason_waiver_btn,
)
from keyboards.inline.callback.constants import BACK_OUTPUT
from keyboards.inline.keypads.general import create_keyboard


def get_back_to_action_kb(number: int) -> InlineKeyboardMarkup:
    return create_keyboard(get_selection_to_edit_btn(number, key=BACK_OUTPUT))


def get_actions_with_habit_kb(number: int) -> InlineKeyboardMarkup:
    return create_keyboard(
        get_my_habits_btn(),
        get_statistics_btn(number),
        get_selection_to_edit_btn(number),
        get_deleting_habit_btn(number),
    )


def get_properties_to_change_kb(number: int, iz_frozen: bool) -> InlineKeyboardMarkup:
    return create_keyboard(
        get_habit_properties_buttons(number, iz_frozen), get_my_habits_btn()
    )


def get_reason_waiver_kb():
    return create_keyboard(get_reason_waiver_btn())


def get_opportunity_to_mark_habit_kb(habit_id: int, date: str):
    return create_keyboard(
        get_tagging_buttons(habit_id=habit_id, date=date), row_width=2
    )
