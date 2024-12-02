from telebot.states import StatesGroup, State


class CreateHabitStates(StatesGroup):
    name = State()
    count = State()
    hour = State()
    description = State()
    save = State()


class ChangeHabitStates(StatesGroup):
    name = State()
    hour = State()


class ReadHabitStates(StatesGroup):
    all_habits = State()
    details = State()
