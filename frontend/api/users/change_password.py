from api.general import make_request
from config import settings
from database.crud.update_token import update_token_by_id


def change_password_by_token(access_token: str, password: str, tg_id: int) -> None:
    """
    Меняет пароль пользователя по его токену
    :param access_token: токен пользователя
    :param password: новый пароль
    :param tg_id: телеграм id для обновления access_token в базе данных
    """
    json = make_request(
        method="patch",
        url=f"http://{settings.api.url}/api/users/change_password/",
        headers={"Authorization": f"Bearer {access_token}"},
        json={"password": password},
    )
    update_token_by_id(telegram_id=tg_id, access_token=json["access_token"])
