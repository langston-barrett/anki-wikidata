from __future__ import annotations

from queries.util import get_results

from ..card import Card

QUERY = """
SELECT DISTINCT ?name ?nSpouse WHERE {
  SERVICE wikibase:label { bd:serviceParam wikibase:language "en_US". }

  {ITEM} wdt:P26 ?spouse .
  ?spouse rdfs:label ?nSpouse .
  filter(lang(?nSpouse) = "en") .

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
            id=f"spouse-{entity[3:]}",
            front=f"What was the name of the spouse of {results[0]['name']}?",
            back=results[0]["nSpouse"],
        )
    ]
