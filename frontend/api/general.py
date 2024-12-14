import logging

import requests
from requests import RequestException

from utils.exceptions import InvalidAccessToken, InvalidApiResponse

logger = logging.getLogger(name=__name__)


def make_request(
    method: str,
    url: str,
    headers: dict[str, str] | None = None,
    json: dict[str, str | int] | None = None,
    params: dict[str, str | int] | None = None,
) -> list[dict] | dict | None:

    try:
        response = requests.request(
            method=method, url=url, headers=headers, json=json, params=params
        )
        if response.status_code == requests.codes.unauthorized:
            raise InvalidAccessToken()
        if response.status_code in (
            requests.codes.not_found,
            requests.codes.unprocessable_entity,
            requests.codes.internal_server_error,
        ):
            logger.error(
                "Ошибка получения корректного ответа: %s",
                response.json().get("detail", "Ошибка api"),
            )
            raise InvalidApiResponse()
        json = response.json()
        return json
    except RequestException as e:
        logger.error("Ошибка соединения с сервером: %s", str(e))
        raise InvalidApiResponse()
