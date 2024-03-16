import json
import logging

import pyarrow as pa
import requests

from models.bootstrap import Bootstrap
from models.element_summary import ElementSummary
from models.fixtures import Fixtures
from pydantic import TypeAdapter
from pydantic.main import BaseModel


logger = logging.getLogger(__name__)


def get_request(url) -> dict:
    logger.info(f"GET {url}")

    r: requests.Response = requests.get(url=url)
    json: dict = r.json()
    return json


def get_request_from_dump(path) -> dict:
    logger.info(f"GET {path}")

    with open(path) as f:
        return json.load(f)


def get_bootstrap() -> Bootstrap:
    # response: dict = get_request(url="https://fantasy.premierleague.com/api/bootstrap-static/")
    response = get_request_from_dump("/Users/colin/projects/fpl2duck/fpl2duck-backend/api/dump/bootstrap.json")
    ta = TypeAdapter(Bootstrap)
    return ta.validate_python(response)


def get_fixtures() -> Fixtures:
    # response: dict = get_request(url="https://fantasy.premierleague.com/api/fixtures/")
    response = get_request_from_dump("/Users/colin/projects/fpl2duck/fpl2duck-backend/api/dump/fixtures.json")
    ta = TypeAdapter(Fixtures)
    return ta.validate_python(response)


def get_element_summary(element_id: int) -> ElementSummary:
    # response: dict = get_request(url=f"https://fantasy.premierleague.com/api/element-summary/{element_id}/")
    response = get_request_from_dump(
        f"/Users/colin/projects/fpl2duck/fpl2duck-backend/api/dump/element-summary-{element_id}.json"
    )
    ta = TypeAdapter(ElementSummary)
    return ta.validate_python(response)


def get_elements() -> list[ElementSummary]:
    bootstrap = get_bootstrap()
    return [get_element_summary(element_id=element["id"]) for element in bootstrap.elements]


def dump_model_to_parquet(model: BaseModel, path: str) -> None:
    logger.info(f"Dumping bootstrap to {path}")

    model.to_parquet(path=path, engine="pyarrow")
    return None


def pydantic_records_to_arrow_table(records: List[BaseModel]) -> pa.Table:
    return pa.Table.from_pylist([record.model_dump() for record in records])
