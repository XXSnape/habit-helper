from api.general import make_request
from config import settings


def mark_habit(
    access_token: str,
    habit_id: int,
    is_done: str,
    date: str,
    reason: str | None = None,
) -> bool:
    """
    Помечает привычку, как выполненную или невыполненную по её id
    :param access_token: токен пользователя
    :param habit_id: id привычки
    :param is_done: 1 или 0, выполнена или нет
    :param date: дата, за которую нужно отметить привычку
    :param reason: причина невыполнения
    :return: результат действия
    """
    json = make_request(
        method="post",
        url=f"http://{settings.api.url}/api/habits/mark/{habit_id}/",
        json={"is_done": bool(int(is_done)), "date": date, "reason": reason},
        headers={"Authorization": f"Bearer {access_token}"},
        error_message="Привычка завершена или удалена",
    )
    return json["completed"]
