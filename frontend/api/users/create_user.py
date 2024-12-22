from api.general import make_request
from config import settings


def get_access_token_for_new_user(
    username: str, password: str, telegram_id: int
) -> str:
    """
    Создает нового пользователя на бэкэнде
    :param username: имя пользователя
    :param password: пароль пользователя
    :param telegram_id: телеграм id
    :return: access_token
    """
    json = make_request(
        method="post",
        url=f"http://{settings.api.url}/api/users/register/",
        json={"username": username, "password": password, "telegram_id": telegram_id},
    )
    return json["access_token"]
