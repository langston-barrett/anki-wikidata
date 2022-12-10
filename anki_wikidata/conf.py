from __future__ import annotations

from typing import List

from pydantic import BaseModel


class Entity(BaseModel):
    id: str
    cards: List[str]


class Config(BaseModel):
    entities: List[Entity]
