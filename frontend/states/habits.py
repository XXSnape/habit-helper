from telebot.states import State, StatesGroup


class CreateHabitStates(StatesGroup):
    """
    Состояния для создания привычки
    """

    name = State()
    count = State()
    hour = State()
    description = State()
    save = State()


class ResumeHabitStates(StatesGroup):
    """
    Состояние для перевода привычки из завершенных в активные
    """

    resume = State()


class ChangeHabitStates(StatesGroup):
    """
    Состояния для смены параметров привычки
    """

    name = State()
    hour = State()
    count = State()
    description = State()


class ReadHabitStates(StatesGroup):
    """
    Состояния для получения информации о привычках
    """

    all_habits = State()
    details = State()


class MarkHabitStates(StatesGroup):
    """
    Состояния для указания причины невыполнения задачи
    """

    reason = State()
