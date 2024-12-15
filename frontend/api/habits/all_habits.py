from api.general import make_request
from config import settings


def get_habits_all_users_by_hour(hour: int):
    json = make_request(
        method="get",
        url=f"http://{settings.api.url}/api/habits/",
        params={"notification_hour": hour},
    )
    return json
