from telebot.types import InlineKeyboardMarkup

from keyboards.inline.buttons.habits import (
    get_my_habits_btn,
    get_selection_to_edit_btn,
    get_habit_properties_buttons,
)
from keyboards.inline.keypads.general import create_keyboard


def get_actions_with_habit_kb(number: int) -> InlineKeyboardMarkup:
    return create_keyboard(get_my_habits_btn(), get_selection_to_edit_btn(number))


def get_properties_to_change_kb(number: int) -> InlineKeyboardMarkup:
    return create_keyboard(get_habit_properties_buttons(number), get_my_habits_btn())
