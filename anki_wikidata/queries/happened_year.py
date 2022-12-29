from __future__ import annotations

from queries.util import get_results

from ..card import Card

QUERY = """
SELECT DISTINCT ?name ?date WHERE {
  SERVICE wikibase:label { bd:serviceParam wikibase:language "en_US". }

  {ITEM} wdt:P585 ?date .

  {ITEM} rdfs:label ?name .
  filter(lang(?name) = "en") .
} 
"""


def query(entity: str) -> list[Card]:
    results = get_results(QUERY.replace("{ITEM}", entity))
    if len(results) != 1:
        return []
    return [
        Card(
            id=f"happened-year-{entity[3:]}",
            front=f"In what year did {results[0]['name']} happen?",
            back=results[0]["date"][:4],
        )
    ]
