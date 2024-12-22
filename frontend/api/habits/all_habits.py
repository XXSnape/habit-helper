from api.general import make_request
from config import settings


def get_habits_all_users_by_hour(hour: int) -> list:
    """
    Получает названия привычек всех пользователей, напоминание о которых должно прийти в hour часов
    :param hour: час, когда нужно отправить напоминание
    :return: список из привычек
    """
    json = make_request(
        method="get",
        url=f"http://{settings.api.url}/api/habits/",
        params={"notification_hour": hour},
    )
    return json
