from telebot.types import InlineKeyboardButton

from keyboards.inline.callback.callbacks import (
    CALL_OFF_CALLBACK,
    REFUSAL_TO_DESCRIBE_CALLBACK,
)
from keyboards.inline.callback.constants import (
    CALL_OFF_OUTPUT,
    REFUSAL_TO_DESCRIBE_OUTPUT,
)


def get_cancel_btn():
    return InlineKeyboardButton(callback_data=CALL_OFF_CALLBACK, text=CALL_OFF_OUTPUT)


def get_cancel_dict():
    return {CALL_OFF_OUTPUT: {"callback_data": CALL_OFF_CALLBACK}}


def get_refusal_to_describe_btn():
    return InlineKeyboardButton(
        text=REFUSAL_TO_DESCRIBE_OUTPUT, callback_data=REFUSAL_TO_DESCRIBE_CALLBACK
    )
