from __future__ import annotations

from queries.util import get_results

from ..card import Card

QUERY = """
SELECT DISTINCT ?name ?nAuthor WHERE {
  SERVICE wikibase:label { bd:serviceParam wikibase:language "en_US". }

  {ITEM} wdt:P50 ?author .
  ?author rdfs:label ?nAuthor .
  filter(lang(?nAuthor) = "en") .

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
            id=f"author-{entity[3:]}",
            front=f"Who wrote \"{results[0]['name']}\"?",
            back=results[0]["nAuthor"],
        )
    ]
