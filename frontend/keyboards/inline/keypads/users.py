from telebot.types import InlineKeyboardMarkup

from keyboards.inline.buttons.cancel import get_cancel_btn
from keyboards.inline.buttons.users import get_freezing_or_defrosting_btn
from keyboards.inline.callback.constants import BACK_OUTPUT
from keyboards.inline.keypads.general import create_keyboard


def get_control_bot_kb(is_active: bool) -> InlineKeyboardMarkup:
    return create_keyboard(
        get_freezing_or_defrosting_btn(is_active), get_cancel_btn(BACK_OUTPUT)
    )
