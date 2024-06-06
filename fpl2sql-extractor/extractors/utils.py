import json
import logging

import pyarrow as pa
import requests

from models.bootstrap import Bootstrap
from models.element_summary import ElementSummary
from models.fixtures import Fixtures
from typing import Union

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


def dump_model_to_parquet(model: Union[Bootstrap, ElementSummary, Fixtures], path: str) -> None:
    logger.info(f"Dumping bootstrap to {path}")

    model.to_parquet(path=path, engine="pyarrow")
    return None


def pydantic_records_to_arrow_table(records: list[Union[Bootstrap, ElementSummary, Fixtures]]) -> pa.Table:
    return pa.Table.from_pylist([record.model_dump() for record in records])
