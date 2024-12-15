from api.general import make_request
from config import settings


def resume_completed_habit(access_token: str, habit_id: int, count: int) -> None:
    make_request(
        method="patch",
        url=f"http://{settings.api.url}/api/habits/resume/{habit_id}/",
        headers={"Authorization": f"Bearer {access_token}"},
        json={"count": count},
        error_message="Привычка уже возобновлена или удалена",
    )
