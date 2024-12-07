from api.general import make_request


def mark_habit(
    access_token: str,
    habit_id: int,
    is_done: bool,
    date: str,
    reason: str | None = None,
) -> bool:
    json = make_request(
        method="post",
        url=f"http://127.0.0.1:8000/api/habits/mark/{habit_id}/",
        json={"is_done": is_done, "date": date, "reason": reason},
        headers={"Authorization": f"Bearer {access_token}"},
    )
    return json["completed"]
