from telebot.handler_backends import State, StatesGroup


class AuthStates(StatesGroup):
    """
    Состояния для регистрации нового пользователя
    """

    username = State()
    password = State()


class LogInStates(StatesGroup):
    """
    Состояния для входа пользователя в существующий аккаунт
    """

    confirmation = State()
    username = State()
    password = State()


class ChangePasswordStates(StatesGroup):
    """
    Состояния для смены пароля
    """

    password = State()
