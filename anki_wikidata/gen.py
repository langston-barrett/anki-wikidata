from __future__ import annotations

from hashlib import sha256
from pathlib import Path
from typing import Any

from genanki import Deck, Model, Note, Package

from .card import Card

ARBITRARY_UNIQUE_ID1 = 1607392419
ARBITRARY_UNIQUE_ID2 = 1607392420

# TODO: The date should appear smaller and in grey.
BASIC_MODEL = Model(
    ARBITRARY_UNIQUE_ID1,
    "Basic",
    fields=[{"name": "Front"}, {"name": "Back"}, {"name": "Reserved"}],
    templates=[
        {
            "name": "Card",
            "qfmt": "{{Front}}",
            "afmt": '{{FrontSide}}<hr id="answer">{{Back}}',
        },
    ],
)


def sha256_int_32(s: str) -> int:
    hash_bytes = sha256(s.encode("utf-8")).digest()[:8]
    hash_int = 0
    for b in hash_bytes:
        hash_int <<= 8
        hash_int += b
    return hash_int % 2_147_483_647


class IdNote(Note):
    def __init__(self, id: str, **kwargs: Any):
        super().__init__(**kwargs)
        self._id = id

    @property
    def guid(self) -> int:
        return sha256_int_32(self._id)


def note(card: Card) -> Note:
    return IdNote(card.id, model=BASIC_MODEL, fields=[card.front, card.back, ""])


def deck(name: str, cards: list[Card]) -> Deck:
    d = Deck(ARBITRARY_UNIQUE_ID2, name)
    for card in cards:
        d.add_note(note(card))
    return d


def write_deck(path: Path, name: str, cards: list[Card]) -> Package:
    pkg = Package(deck(name, cards))
    pkg.write_to_file(str(path))
