from api.general import make_request
from config import settings
from utils.cache_keys import HABITS_KEY
from utils.output import get_text_from_cache


def get_my_habits_by_token(
    access_token: str, cache: dict, is_complete_null: bool
) -> str | None:
    """
    Получает полную информацию о привычках пользователя по его access_token.
    Кэширует полученную информацию, кладя ее в список с первым элементом None,
    чтобы номер привычки от пользователя совпадал с её фактическим индексом в кэше

    :param access_token: токен пользователя
    :param cache: кэш
    :param is_complete_null: True или False, должны привычки быть действующими или завершёнными
    :return: информация о привычках или None, если их нет
    """
    json = make_request(
        method="get",
        url=f"http://{settings.api.url}/api/habits/me/",
        headers={"Authorization": f"Bearer {access_token}"},
        params={"is_complete_null": is_complete_null},
    )
    if not json:
        return None
    json.insert(0, None)
    cache[HABITS_KEY] = json
    return get_text_from_cache(cache=cache)
