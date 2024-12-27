from inline.buttons.cancel import get_home_btn
from inline.buttons.habits import (
    get_deleting_habit_btn,
    get_habit_details_btn,
    get_habit_properties_buttons,
    get_my_habits_btn,
    get_reason_waiver_btn,
    get_resuming_btn,
    get_selection_to_edit_btn,
    get_statistics_btn,
    get_tagging_buttons,
)
from inline.callback.constants import BACK_OUTPUT, MENU_OUTPUT
from inline.keypads.general import create_keyboard
from telebot.types import InlineKeyboardMarkup


def get_back_to_action_kb(number: int) -> InlineKeyboardMarkup:
    """
    Возвращает клавиатуру для того, чтобы вернуться к редактированию привычки
    :param number: номер привычки в кэше
    :return: InlineKeyboardMarkup
    """
    return create_keyboard(get_selection_to_edit_btn(number, key=BACK_OUTPUT))


def get_actions_with_habit_kb(number: int) -> InlineKeyboardMarkup:
    """
    Возвращает клавиатуру с возможными действиями с привычкой:
    - просмотр статистики
    - редактирование
    :param number: номер привычки в кэше
    :return: InlineKeyboardMarkup
    """
    return create_keyboard(
        get_statistics_btn(number),
        get_selection_to_edit_btn(number),
        get_deleting_habit_btn(number),
        get_my_habits_btn(),
        get_home_btn(MENU_OUTPUT),
    )


def get_actions_with_completed_habit_kb(number: int) -> InlineKeyboardMarkup:
    """
    Возвращает возможные действия с завершенной привычкой
    :param number: номер привычки в кэше
    :return: InlineKeyboardMarkup
    """
    return create_keyboard(
        get_my_habits_btn(),
        get_statistics_btn(number),
        get_resuming_btn(number),
        get_deleting_habit_btn(number),
        get_home_btn(MENU_OUTPUT),
    )


def get_back_to_habits_details_and_menu(number: int) -> InlineKeyboardMarkup:
    """
    Возвращает клавиатуру для возвращения к деталям привычки
    :param number: номер привычки в кэше
    :return: InlineKeyboardMarkup
    """
    return create_keyboard(get_my_habits_btn(), get_habit_details_btn(number))


def get_back_to_habits_kb() -> InlineKeyboardMarkup:
    """
    Возвращает клавиатуру для возврата к списку привычек
    :return:
    """
    return create_keyboard(get_my_habits_btn())


def get_properties_to_change_kb(number: int, iz_frozen: bool) -> InlineKeyboardMarkup:
    """
    Возвращает клавиатуру с параметрами для редактирования и возврату к предыдущим стадиям
    :param number: номер привычки в кэше
    :param iz_frozen: приостановлена текущая привычка или нет
    :return: InlineKeyboardMarkup
    """
    return create_keyboard(
        get_habit_properties_buttons(number, iz_frozen),
        get_habit_details_btn(number),
        get_my_habits_btn(),
        get_home_btn(MENU_OUTPUT),
    )


def get_reason_waiver_kb() -> InlineKeyboardMarkup:
    """
    Возвращает клавиатуру, чтобы отказаться задавать причину невыполения задачи
    :return: InlineKeyboardMarkup
    """
    return create_keyboard(get_reason_waiver_btn())


def get_opportunity_to_mark_habit_kb(habit_id: int, date: str) -> InlineKeyboardMarkup:
    """
    Возвращает клавиатуру для пометки задачи как выполненную или нет
    :param habit_id: id привычки на бэкэнде
    :param date: дата, за которую нужно отметить задачу
    :return: InlineKeyboardMarkup
    """
    return create_keyboard(
        get_tagging_buttons(habit_id=habit_id, date=date), row_width=2
    )
