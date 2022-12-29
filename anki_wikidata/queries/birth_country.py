from __future__ import annotations

from queries.util import get_results

from ..card import Card

QUERY = """
SELECT DISTINCT ?name ?nCountry WHERE {
  SERVICE wikibase:label { bd:serviceParam wikibase:language "en_US". }

  {ITEM} wdt:P19 ?place .
  ?place wdt:P17 ?country .
  ?country rdfs:label ?nCountry .
  filter(lang(?nCountry) = "en") .

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
            id=f"birth-country-{entity[3:]}",
            front=f"In what country was {results[0]['name']} born?",
            back=results[0]["nCountry"],
        )
    ]
