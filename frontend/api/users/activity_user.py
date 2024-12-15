from api.general import make_request
from config import settings


def activate_or_deactivate_user_by_flag(access_token: str, is_active: bool) -> None:
    make_request(
        method="patch",
        url=f"http://{settings.api.url}/api/users/change_activity/",
        headers={"Authorization": f"Bearer {access_token}"},
        json={"is_active": is_active},
    )
