from api.general import make_request
from utils.constants import HABITS_KEY
from utils.output import get_text_from_cache


def get_my_habits_by_token(access_token: str, data: dict) -> str | None:
    json = make_request(
        method="get",
        url="http://127.0.0.1:8000/api/habits/me/",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    if not json:
        return None
    json.insert(0, None)
    print("j", json)
    data[HABITS_KEY] = json
    return get_text_from_cache(data=data)
