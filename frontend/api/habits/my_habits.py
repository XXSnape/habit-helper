from api.general import make_request
from config import settings
from utils.cache_keys import HABITS_KEY
from utils.output import get_text_from_cache


def get_my_habits_by_token(
    access_token: str, cache: dict, is_complete_null: bool
) -> str | None:
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
