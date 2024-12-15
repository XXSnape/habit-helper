from api.general import make_request
from config import settings


def create_new_habit(
    access_token: str, name: str, count: int, hour: int, description: str
) -> bool:
    json = make_request(
        method="post",
        url=f"http://{settings.api.url}/api/habits/",
        headers={"Authorization": f"Bearer {access_token}"},
        json={
            "name": name,
            "notification_hour": hour,
            "count": count,
            "description": description,
        },
    )
    return json["result"]
