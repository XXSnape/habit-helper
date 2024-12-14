from api.general import make_request


def mark_habit(
    access_token: str,
    habit_id: int,
    is_done: str,
    date: str,
    reason: str | None = None,
) -> bool:
    json = make_request(
        method="post",
        url=f"http://127.0.0.1:8000/api/habits/mark/{habit_id}/",
        json={"is_done": bool(int(is_done)), "date": date, "reason": reason},
        headers={"Authorization": f"Bearer {access_token}"},
        error_message="Привычка завершена или удалена",
    )
    return json["completed"]
