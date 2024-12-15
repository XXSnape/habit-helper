from keyboards.inline.buttons.cancel import get_home_btn
from keyboards.inline.callback.callbacks import (
    REGISTRATION_CALLBACK,
    CB,
    LOG_IN_CALLBACK,
)
from keyboards.inline.callback.constants import (
    REGISTER_OUTPUT,
    LOG_IN_OUTPUT,
    MENU_OUTPUT,
)


def get_check_in_buttons():
    return {
        REGISTER_OUTPUT: {CB: REGISTRATION_CALLBACK},
        LOG_IN_OUTPUT: {CB: LOG_IN_CALLBACK},
        **get_home_btn(MENU_OUTPUT),
    }
