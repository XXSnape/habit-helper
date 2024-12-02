from telebot.types import InlineKeyboardMarkup

from keyboards.inline.buttons.cancel import get_cancel_btn
from keyboards.inline.buttons.habits import get_selection_to_edit_btn
from keyboards.inline.buttons.time import get_hours_buttons
from keyboards.inline.callback.constants import BACK_OUTPUT
from keyboards.inline.keypads.general import create_keyboard


def get_hour_selection_kb() -> InlineKeyboardMarkup:

    return create_keyboard(get_hours_buttons(), get_cancel_btn(), row_width=4)


def get_hour_selection_and_back_kb(number: int) -> InlineKeyboardMarkup:
    return create_keyboard(
        get_hours_buttons(),
        get_selection_to_edit_btn(number, key=BACK_OUTPUT),
        row_width=4,
    )
