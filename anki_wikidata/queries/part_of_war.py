from __future__ import annotations

from queries.util import get_results

from ..card import Card

# TODO: Allow subclass of war
QUERY = """
SELECT DISTINCT ?name ?nWar WHERE {
  SERVICE wikibase:label { bd:serviceParam wikibase:language "en_US". }

  {ITEM} wdt:P361 ?war .
  ?war wdt:P31 wd:Q198 .
  ?war rdfs:label ?nWar .
  filter(lang(?nWar) = "en") .

  {ITEM} rdfs:label ?name .
  filter(lang(?name) = "en") .
}
"""


def query(entity: str) -> list[Card]:
    assert "{ITEM}" in QUERY
    results = get_results(QUERY.replace("{ITEM}", entity))
    if len(results) != 1:
        return []
    return [
        Card(
            id=f"part-of-war-{entity[3:]}",
            front=f"What war was the {results[0]['name']} part of?",
            back=results[0]["nWar"],
        )
    ]
