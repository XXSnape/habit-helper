from logging import getLogger

from api.general import make_request
from config import settings
from database.crud.update_token import update_telegram_id_and_token
from utils.exceptions import InvalidAccessToken

logger = getLogger(__name__)


def change_telegram_id_by_credentials(
    username: str, password: str, new_telegram_id: int
) -> bool:
    """
    Меняет telegram id по никнейму и паролю на бэкэнде и в базе данных
    :param username: имя пользователя
    :param password: пароль пользователя
    :param new_telegram_id: новый telegram id
    :return: False при безуспешной авторизации на сервисе или True
    """
    try:
        json = make_request(
            method="patch",
            url=f"http://{settings.api.url}/api/users/change_telegram_id/",
            json={
                "username": username,
                "password": password,
                "telegram_id": new_telegram_id,
            },
        )
        update_telegram_id_and_token(
            old_telegram_id=json["telegram_id"],
            new_telegram_id=new_telegram_id,
            access_token=json["access_token"],
        )
        return True

    except InvalidAccessToken:
        logger.info("Пользователь %s не прошел авторизацию", new_telegram_id)
        return False
