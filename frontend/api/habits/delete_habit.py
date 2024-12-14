from api.general import make_request
from utils.constants import HABITS_KEY
from utils.output import get_text_from_cache


def delete_habit_by_id(access_token: str, number: int, data: dict):
    habit_id = data[HABITS_KEY][number]["id"]
    make_request(
        method="delete",
        url=f"http://127.0.0.1:8000/api/habits/{habit_id}/",
        headers={"Authorization": f"Bearer {access_token}"},
        error_message="Привычка уже удалена",
    )
    data[HABITS_KEY].pop(number)
    return get_text_from_cache(data)
