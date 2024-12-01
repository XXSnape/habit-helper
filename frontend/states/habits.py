from telebot.states import StatesGroup, State


class HabitsStates(StatesGroup):
    name = State()
    count = State()
    hour = State()
    description = State()
    save = State()
