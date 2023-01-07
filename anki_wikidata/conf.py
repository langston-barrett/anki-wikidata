from __future__ import annotations

from typing import Optional, List

from pydantic import BaseModel


class Entity(BaseModel):
    id: str
    tags: List[str]
    cards: List[str]
    name: Optional[str] = None


class Config(BaseModel):
    id: int
    entities: List[Entity]
