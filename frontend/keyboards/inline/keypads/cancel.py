from telebot.types import InlineKeyboardMarkup

from .general import create_keyboard
from ..buttons.cancel import (
    get_home_btn,
    get_refusal_to_describe_btn,
    get_home_btn,
)
from ..callback.constants import CALL_OFF_OUTPUT


def get_cancel_kb(output=CALL_OFF_OUTPUT) -> InlineKeyboardMarkup:
    return create_keyboard(get_home_btn(output))


def get_refusal_to_describe_kb():
    return create_keyboard(get_refusal_to_describe_btn(), get_home_btn())
