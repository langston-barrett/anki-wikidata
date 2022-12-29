from __future__ import annotations

from queries.util import get_results

from ..card import Card

QUERY = """
SELECT DISTINCT ?name ?nManner WHERE {
  SERVICE wikibase:label { bd:serviceParam wikibase:language "en_US". }

  {ITEM} wdt:P1196 ?manner .
  ?manner rdfs:label ?nManner .
  filter(lang(?nManner) = "en") .

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
            id=f"manner-of-death-{entity[3:]}",
            front=f"What was the manner of death of {results[0]['name']}?",
            back=results[0]["nManner"],
        )
    ]
