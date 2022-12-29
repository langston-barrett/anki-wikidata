from dataclasses import dataclass, field
from typing import List


@dataclass
class Card:
    id: str
    front: str
    back: str
    tags: List[str] = field(default_factory=list)
