from keyboards.callbacks import REGISTRATION
from keyboards.general import create_keyboard


def get_auth_request():
    buttons = [["Зарегистрироваться", REGISTRATION]]
    return create_keyboard(buttons)
