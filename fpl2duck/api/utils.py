import requests

from api.types.bootstrap import Bootstrap, bootstrap_from_dict
import logging

logger = logging.getLogger(__name__)


def get_request(url) -> dict:

    logger.info(f"GET {url}")

    r: requests.Response = requests.get(url=url)
    json: dict = r.json()
    return json


def get_bootstrap() -> Bootstrap:

    response: dict = get_request(url="https://fantasy.premierleague.com/api/bootstrap-static/")
    return bootstrap_from_dict(response)
