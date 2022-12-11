from __future__ import annotations

from queries.util import get_results

from ..card import Card

QUERY = """
SELECT DISTINCT ?nBorough ?nPlace WHERE {
  SERVICE wikibase:label { bd:serviceParam wikibase:language "en_US". }

  {ITEM} wdt:P131 ?borough .
  ?borough wdt:P31 wd:Q408804 .

  ?borough rdfs:label ?nBorough .
  filter(lang(?nBorough) = "en") .

  {ITEM} rdfs:label ?nPlace .
  filter(lang(?nPlace) = "en") .
} 
"""


def query(entity: str) -> list[Card]:
    assert "{ITEM}" in QUERY
    results = get_results(QUERY.replace("{ITEM}", entity))
    if len(results) != 1:
        return []
    return [
        Card(
            id=f"borough-{entity}",
            front=f"'{results[0]['nPlace']}' is part of which borough?",
            back=results[0]["nBorough"],
        )
    ]
