from api.general import make_request
from config import settings


def get_new_access_token_by_id(telegram_id: int) -> str:
    """
    Получает новый access_token по telegram_id
    :param telegram_id: телеграм id
    :return: новый access_token
    """
    json = make_request(
        method="post",
        url=f"http://{settings.api.url}/api/users/new/",
        json={"telegram_id": telegram_id},
    )
    return json["access_token"]
