from dataclasses import dataclass, field


@dataclass(frozen=True)
class Card:
    id: str
    front: str
    back: str
