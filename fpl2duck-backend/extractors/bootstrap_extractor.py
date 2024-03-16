import logging

from models.bootstrap import Bootstrap
from pydantic import BaseModel, TypeAdapter
from extractors.utils import get_request_from_dump
from extractors.utils import get_request

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def get_bootstrap() -> Bootstrap:
    response: dict = get_request(url="https://fantasy.premierleague.com/api/bootstrap-static/")
    # response = get_request_from_dump("/Users/colin/projects/fpl2duck/fpl2duck-backend/dump/bootstrap.json")
    ta = TypeAdapter(Bootstrap)
    return ta.validate_python(response)


class TotalPlayers(BaseModel):
    total_players: int


def get_bootstrap_tables():
    logger.info("Getting Bootstrap records")
    bootstrap: Bootstrap = get_bootstrap()

    return {
        "events": bootstrap.events,
        "game_settings": [bootstrap.game_settings],
        "phases": bootstrap.phases,
        "teams": bootstrap.teams,
        "total_players": [TotalPlayers(total_players=bootstrap.total_players)],
        "elements": bootstrap.elements,
        "element_stats": bootstrap.element_stats,
        "element_types": bootstrap.element_types,
    }
