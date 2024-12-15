from api.general import make_request


def get_habit_name(access_token: str, habit_id: int) -> str:
    json = make_request(
        method="get",
        url=f"http://127.0.0.1:8000/api/habits/{habit_id}/",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    return json["name"]
