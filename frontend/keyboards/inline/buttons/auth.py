from telebot.types import InlineKeyboardButton

from keyboards.inline.callback.callbacks import (
    REGISTRATION_CALLBACK,
    DELETE_CALLBACK,
    CB,
    LOG_IN_CALLBACK,
)
from keyboards.inline.callback.constants import (
    REGISTER_OUTPUT,
    DELETE_MSG_OUTPUT,
    LOG_IN_OUTPUT,
)


def get_check_in_buttons():
    return {
        REGISTER_OUTPUT: {CB: REGISTRATION_CALLBACK},
        LOG_IN_OUTPUT: {CB: LOG_IN_CALLBACK},
    }
