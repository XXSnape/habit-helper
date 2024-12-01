from api.general import make_request


def create_new_habit(
    access_token: str, name: str, count: int, hour: int, description: str
) -> bool:
    json = make_request(
        method="post",
        url="http://127.0.0.1:8000/api/habits/",
        headers={"Authorization": f"Bearer {access_token}"},
        json={
            "name": name,
            "notification_hour": hour,
            "count": count,
            "description": description,
        },
    )
    return json["result"]
