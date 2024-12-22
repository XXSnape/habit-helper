from api.general import make_request
from config import settings
from utils.cache_keys import HABITS_KEY
from utils.output import get_habit_details_from_cache


def update_habit(access_token: str, number: int, new_data: dict, cache: dict) -> str:
    habit_id = cache[HABITS_KEY][number]["id"]
    make_request(
        method="patch",
        url=f"http://{settings.api.url}/api/habits/{habit_id}",
        headers={"Authorization": f"Bearer {access_token}"},
        json=new_data,
        error_message="Привычка удалена",
    )
    cache[HABITS_KEY][number].update(new_data)
    return get_habit_details_from_cache(
        cache=cache, number=number, initial_text="Привычка успешно обновлена!"
    )
