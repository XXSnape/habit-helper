import logging

import requests
from requests import RequestException

from utils.exceptions import InvalidAccessToken

logger = logging.getLogger(name=__name__)


def make_request(
    method: str,
    url: str,
    headers: dict[str, str] | None = None,
    json: dict[str, str | int] | None = None,
    params: dict[str, str] | None = None,
) -> list[dict] | dict | None:

    try:
        response = requests.request(
            method=method, url=url, headers=headers, json=json, params=params
        )
        if response.status_code == requests.codes.unauthorized:
            raise InvalidAccessToken()
        j = response.json()
        print(response.status_code)
        print("json", j)
        return j
    except RequestException as e:
        logger.error(str(e))
        return None
