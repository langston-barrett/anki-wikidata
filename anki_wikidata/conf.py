from __future__ import annotations

from typing import Optional, List

from pydantic import BaseModel


class Entity(BaseModel):
    id: str
    tags: List[str]
    cards: List[str]
    name: Optional[str] = None


# TODO
class Relation(BaseModel):
    relation: str
    entities: List[str]
    tags: List[str]


class Config(BaseModel):
    id: int
    entities: List[Entity]
    relations: List[Relation]
