import logging

import requests
from requests import RequestException

logger = logging.getLogger(name=__name__)


def make_request(
    method: str,
    url: str,
    headers: dict[str, str] | None = None,
    json: dict[str, str] | None = None,
    params: dict[str, str] | None = None,
) -> dict | None:

    try:
        response = requests.request(
            method=method, url=url, headers=headers, json=json, params=params
        )
        j = response.json()
        print("json", j)
        return j
    except RequestException as e:
        logger.error(str(e))
        return None
