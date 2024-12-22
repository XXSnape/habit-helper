from api.general import make_request
from config import settings
from utils.cache_keys import HABITS_KEY
from utils.output import get_text_from_cache


def delete_habit_by_number(access_token: str, number: int, cache: dict) -> str | None:
    """
    Удаляет привычку по id, получая его из кэша по номеру, обновляет кэш
    :param access_token: токен пользователя
    :param number: номер в кэше
    :param cache: кэш
    :return: информация об оставшихся привычках или None
    """
    habit_id = cache[HABITS_KEY][number]["id"]
    make_request(
        method="delete",
        url=f"http://{settings.api.url}/api/habits/{habit_id}/",
        headers={"Authorization": f"Bearer {access_token}"},
        error_message="Привычка уже удалена",
    )
    cache[HABITS_KEY].pop(number)
    return get_text_from_cache(cache)
