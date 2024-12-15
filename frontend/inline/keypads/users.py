from telebot.types import InlineKeyboardMarkup

from inline.buttons.cancel import get_home_btn
from inline.buttons.users import get_freezing_or_defrosting_btn
from inline.callback.constants import BACK_OUTPUT
from inline.keypads.general import create_keyboard


def get_control_bot_kb(is_active: bool) -> InlineKeyboardMarkup:
    return create_keyboard(
        get_freezing_or_defrosting_btn(is_active), get_home_btn(BACK_OUTPUT)
    )
