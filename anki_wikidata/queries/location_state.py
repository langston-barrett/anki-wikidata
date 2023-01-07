from __future__ import annotations

from queries.util import get_results

from ..card import Card

QUERY = """
SELECT DISTINCT ?name ?nState WHERE {
  SERVICE wikibase:label { bd:serviceParam wikibase:language "en_US". }

  {ITEM} wdt:P276 ?place .
  ?place (wdt:P131|wdt:P361)* ?state .
  ?state wdt:P31 wd:Q35657 .
  ?state rdfs:label ?nState .
  filter(lang(?nState) = "en") .

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
            id=f"location-state-{entity[3:]}",
            front=f"In what US state was the {results[0]['name']}?",
            back=results[0]["nState"],
        )
    ]
