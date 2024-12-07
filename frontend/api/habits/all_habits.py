from api.general import make_request


def get_habits_all_users_by_hour(hour: int):
    json = make_request(
        method="get",
        url="http://127.0.0.1:8000/api/habits/",
        params={"notification_hour": hour},
    )
    return json
