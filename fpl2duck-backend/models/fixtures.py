# generated by datamodel-codegen:
#   filename:  fixtures.json
#   timestamp: 2024-03-16T11:32:20+00:00

from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel, RootModel


class AItem(BaseModel):
    value: int
    element: int


class HItem(BaseModel):
    value: int
    element: int


class Stat(BaseModel):
    identifier: str
    a: List[AItem]
    h: List[HItem]


class ModelItem(BaseModel):
    code: int
    event: Optional[int]
    finished: bool
    finished_provisional: bool
    id: int
    kickoff_time: Optional[str]
    minutes: int
    provisional_start_time: bool
    started: Optional[bool]
    team_a: int
    team_a_score: Optional[int]
    team_h: int
    team_h_score: Optional[int]
    stats: List[Stat]
    team_h_difficulty: int
    team_a_difficulty: int
    pulse_id: int


class Fixtures(RootModel):
    root: List[ModelItem]
