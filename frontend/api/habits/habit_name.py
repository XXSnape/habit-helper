from api.general import make_request
from config import settings


def get_habit_name(access_token: str, habit_id: int) -> str:
    json = make_request(
        method="get",
        url=f"http://{settings.api.url}/api/habits/{habit_id}/",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    return json["name"]
