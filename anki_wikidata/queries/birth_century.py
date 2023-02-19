from __future__ import annotations

from queries.util import get_results

from ..card import Card

QUERY = """
SELECT DISTINCT ?name ?date WHERE {
  SERVICE wikibase:label { bd:serviceParam wikibase:language "en_US". }

  {ITEM} wdt:P569 ?date .

  {ITEM} rdfs:label ?name .
  filter(lang(?name) = "en") .
} 
"""


def query(entity: str) -> list[Card]:
    results = get_results(QUERY.replace("{ITEM}", entity))
    if len(results) != 1:
        return []
    date = results[0]['date']
    year = int(date[:4])
    if date.startswith("-"):
        year = int(date[:5])
    if year < 0:
        year += abs(year) % 100
    else:
        year -= abs(year) % 100
    return [
        Card(
            id=f"birth-century-{entity[3:]}",
            front=f"In what century was {results[0]['name']} born?",
            back=f"The {abs(year)}s {'B.C.E' if year < 0 else 'C.E.'}",
        )
    ]
