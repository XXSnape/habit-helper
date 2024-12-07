from telebot.handler_backends import StatesGroup, State


class AuthStates(StatesGroup):
    username = State()
    password = State()


class LogInStates(StatesGroup):
    confirmation = State()
    username = State()
    password = State()
