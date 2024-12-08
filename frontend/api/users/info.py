from api.general import make_request
from utils.output import get_my_info_from_json


def get_my_info_by_token(access_token: str) -> tuple[str, bool]:
    json = make_request(
        method="get",
        url="http://127.0.0.1:8000/api/users/me/",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    return get_my_info_from_json(data=json), json["is_active"]
