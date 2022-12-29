from __future__ import annotations

from queries.util import get_results

from ..card import Card

QUERY = """
SELECT DISTINCT ?name ?nPlace WHERE {
  SERVICE wikibase:label { bd:serviceParam wikibase:language "en_US". }

  {ITEM} wdt:P20 ?place .
  ?place rdfs:label ?nPlace .

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
            id=f"place-of-death-{entity[3:]}",
            front=f"Where did {results[0]['name']} die?",
            back=results[0]["nPlace"],
        )
    ]
