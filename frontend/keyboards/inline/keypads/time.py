from telebot.types import InlineKeyboardMarkup

from keyboards.inline.buttons.cancel import get_cancel_btn
from keyboards.inline.buttons.time import get_hours_buttons
from keyboards.inline.keypads.general import create_keyboard


def get_hour_selection_kb() -> InlineKeyboardMarkup:

    return create_keyboard(get_hours_buttons(), get_cancel_btn(), row_width=4)
