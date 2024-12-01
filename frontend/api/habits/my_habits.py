from api.general import make_request


def get_my_habits_by_token(access_token: str):
    json = make_request(
        method="get",
        url="http://127.0.0.1:8000/api/habits/me/",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    return json
