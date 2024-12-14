from keyboards.inline.buttons.auth import get_check_in_buttons
from keyboards.inline.buttons.cancel import get_home_btn, get_home_btn
from keyboards.inline.callback.callbacks import REGISTRATION_CALLBACK
from keyboards.inline.keypads.general import create_keyboard


def get_auth_request_kb():
    return create_keyboard(get_check_in_buttons())


def delete_password_request_kb():
    return create_keyboard(get_home_btn())
