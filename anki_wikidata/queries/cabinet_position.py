from __future__ import annotations

from queries.util import get_results

from ..card import Card

QUERY = """
SELECT DISTINCT ?name ?nPos WHERE {
  SERVICE wikibase:label { bd:serviceParam wikibase:language "en_US". }

  {ITEM} wdt:P39 ?pos .
  ?pos wdt:P31 wd:Q639738 .
  ?pos rdfs:label ?nPos .
  filter(lang(?nPos) = "en") .

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
            id=f"part-of-war-{entity[3:]}",
            front=f"What cabinet position did {results[0]['name']} hold?",
            back=results[0]["nPos"],
        )
    ]
