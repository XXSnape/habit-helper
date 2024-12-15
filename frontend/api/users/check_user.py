from api.general import make_request
from config import settings


def check_user_existence(username: str) -> bool:
    json = make_request(
        method="get",
        url=f"http://{settings.api.url}/api/users/",
        params={"username": username},
    )
    return json["result"]
