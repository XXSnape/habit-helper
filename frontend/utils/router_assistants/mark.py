from api.habits.mark_habit import mark_habit
from database.crud.check_user import get_user_token
from inline.callback.factories import mark_habit_factory
from telebot.types import CallbackQuery
from utils.refresh_token import get_response_and_refresh_token


def get_data_on_completion_habit(callback: CallbackQuery) -> bool:
    """
    Получает информацию о том, было ли выполнение задания последним
    для его завершения
    :param callback: CallbackQuery
    :return: задание завершено или нет
    """
    mark_habit_data = mark_habit_factory.parse(callback.data)
    mark_habit_data.pop("@")
    token = get_user_token(callback.from_user.id)
    return get_response_and_refresh_token(
        telegram_id=callback.from_user.id,
        func=mark_habit,
        access_token=token,
        **mark_habit_data,
    )
