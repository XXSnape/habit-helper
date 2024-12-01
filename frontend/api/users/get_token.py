from api.general import make_request


def get_new_access_token_by_id(telegram_id: int) -> str:
    json = make_request(
        method="post",
        url="http://127.0.0.1:8000/api/users/new/",
        json={"telegram_id": telegram_id},
    )
    return json["access_token"]
