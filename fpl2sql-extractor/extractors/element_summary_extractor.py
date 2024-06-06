import logging

from pydantic import  TypeAdapter
from extractors.utils import get_request_from_dump
from models.element_summary import ElementSummary
from extractors.bootstrap_extractor import get_bootstrap
from itertools import chain
from extractors.utils import get_request


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

def get_element_summary(element_id: int) -> ElementSummary:
    response: dict = get_request(url=f"https://fantasy.premierleague.com/api/element-summary/{element_id}/")
    # response = get_request_from_dump(
    #     f"/Users/colin/projects/fpl2duck/fpl2duck-backend/dump/element-summary-1.json"
    # )
    ta = TypeAdapter(ElementSummary)
    return ta.validate_python(response)


def get_elements() -> list[ElementSummary]:
    bootstrap = get_bootstrap()
    element_ids = [element.id for element in bootstrap.elements]
    logger.info(f"Getting ElementSummary records for {len(element_ids)} elements")

    return [get_element_summary(element_id=element_id) for element_id in element_ids]


def get_element_summary_table():
    elements: list[ElementSummary] = get_elements()

    return {
        "element_history":  chain.from_iterable([element.history for element in elements]),
        "element_history_past": chain.from_iterable([element.history_past for element in elements])
    }
