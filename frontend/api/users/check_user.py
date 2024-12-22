from api.general import make_request
from config import settings


def check_user_existence(username: str) -> bool:
    """
    Проверяет, существует ли пользователь с username на бэкэнде
    :param username: имя пользователя
    :return: True, если существует, иначе False
    """
    json = make_request(
        method="get",
        url=f"http://{settings.api.url}/api/users/",
        params={"username": username},
    )
    return json["result"]
