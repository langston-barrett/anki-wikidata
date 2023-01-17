
from __future__ import annotations

from queries.util import get_results

from ..card import Card

QUERY = """
SELECT DISTINCT ?name ?date WHERE {
  SERVICE wikibase:label { bd:serviceParam wikibase:language "en_US". }

  {ITEM} wdt:P577 ?date .

  {ITEM} rdfs:label ?name .
  filter(lang(?name) = "en") .
}
"""


def query(entity: str) -> list[Card]:
    results = get_results(QUERY.replace("{ITEM}", entity))
    if len(results) == 0:
        return []
    if len(results) > 1:
        results = sorted(results, key=lambda r: int(r["date"][:4]))
    return [
        Card(
            id=f"first-publication-year-{entity[3:]}",
            front=f"In what year was {results[0]['name']} first published?",
            back=results[0]["date"][:4],
        )
    ]
