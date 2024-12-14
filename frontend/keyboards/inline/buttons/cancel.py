from telebot.types import InlineKeyboardButton

from keyboards.inline.callback.callbacks import (
    CALL_OFF_CALLBACK,
    REFUSAL_TO_DESCRIBE_CALLBACK,
    CB,
)
from keyboards.inline.callback.constants import (
    CALL_OFF_OUTPUT,
    REFUSAL_TO_DESCRIBE_OUTPUT,
)


def get_home_btn(output=CALL_OFF_OUTPUT):
    return {output: {CB: CALL_OFF_CALLBACK}}


def get_refusal_to_describe_btn():
    return {REFUSAL_TO_DESCRIBE_OUTPUT: {CB: REFUSAL_TO_DESCRIBE_CALLBACK}}
