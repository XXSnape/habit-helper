from api.general import make_request
from config import settings


def activate_or_deactivate_user_by_flag(access_token: str, is_active: bool) -> None:
    """
    Активирует или деактивирует пользователя.
    Если пользователь неактивен, ему не приходят напоминания о привычках
    :param access_token: токен пользователя
    :param is_active: статус активности пользователя
    """
    make_request(
        method="patch",
        url=f"http://{settings.api.url}/api/users/change_activity/",
        headers={"Authorization": f"Bearer {access_token}"},
        json={"is_active": is_active},
    )
