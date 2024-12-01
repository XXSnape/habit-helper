from api.general import make_request


def create_user(username: str, password: str, telegram_id: int) -> str:
    json = make_request(
        method="post",
        url="http://127.0.0.1:8000/api/users/register/",
        json={"username": username, "password": password, "telegram_id": telegram_id},
    )
    return json["access_token"]
