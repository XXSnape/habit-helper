from api.general import make_request
from config import settings


def create_new_habit(
    access_token: str, name: str, count: int, hour: int, description: str
) -> bool:
    """
    Создает новую привычку
    :param access_token: токен пользователя
    :param name: название
    :param count: количество повторений
    :param hour: час для напоминания
    :param description: описание
    :return: результат создания
    """
    json = make_request(
        method="post",
        url=f"http://{settings.api.url}/api/habits/",
        headers={"Authorization": f"Bearer {access_token}"},
        json={
            "name": name,
            "notification_hour": hour,
            "count": count,
            "description": description,
        },
    )
    return json["result"]
