from __future__ import annotations

from typing import List

from pydantic import BaseModel


class Entity(BaseModel):
    id: str
    tags: List[str]
    cards: List[str]


class Config(BaseModel):
    id: int
    entities: List[Entity]
