from __future__ import annotations

from queries.util import get_results

from ..card import Card

QUERY = """
SELECT DISTINCT ?name ?nWinner WHERE {
  SERVICE wikibase:label { bd:serviceParam wikibase:language "en_US". }

  {ITEM} wdt:P991 ?winner .
  ?winner rdfs:label ?nWinner .
  filter(lang(?nWinner) = "en") .

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
            id=f"winner-{entity[3:]}",
            front=f"What was the name of the winner of the {results[0]['name']}?",
            back=results[0]["nWinner"],
        )
    ]
