from api.general import make_request


def check_user_existence(username: str) -> bool:
    json = make_request(
        method="get",
        url="http://127.0.0.1:8000/api/users/",
        params={"username": username},
    )
    return json["result"]
