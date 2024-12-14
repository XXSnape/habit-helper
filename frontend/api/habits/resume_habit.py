from api.general import make_request


def resume_completed_habit(access_token: str, habit_id: int, count: int) -> None:
    make_request(
        method="patch",
        url=f"http://127.0.0.1:8000/api/habits/resume/{habit_id}/",
        headers={"Authorization": f"Bearer {access_token}"},
        json={"count": count},
        error_message="Привычка уже возобновлена или удалена",
    )
