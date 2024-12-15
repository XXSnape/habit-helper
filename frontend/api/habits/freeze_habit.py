from api.general import make_request


def freeze_habit_by_id(access_token: str, habit_id: int) -> None:
    make_request(
        method="patch",
        url=f"http://127.0.0.1:8000/api/habits/{habit_id}",
        headers={"Authorization": f"Bearer {access_token}"},
        json={"is_frozen": True},
        error_message="Привычка удалена",
    )
