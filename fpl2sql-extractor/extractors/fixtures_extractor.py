import logging

from models.fixtures import Fixtures
from extractors.utils import get_request_from_dump
from pydantic import TypeAdapter
from extractors.utils import get_request

logger = logging.getLogger(__name__)


def get_fixtures() -> Fixtures:
    response: dict = get_request(url="https://fantasy.premierleague.com/api/fixtures/")
    # response = get_request_from_dump("/Users/colin/projects/fpl2duck/fpl2duck-backend/dump/fixtures.json")
    ta = TypeAdapter(Fixtures)
    return ta.validate_python(response)

def get_fixtures_table():
    logger.info("Getting Fixtures records")
    fixtures: Fixtures = get_fixtures()

    return {
        "fixtures": fixtures.root
    }
