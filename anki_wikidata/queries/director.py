from __future__ import annotations

from queries.util import get_results

from ..card import Card

QUERY = """
SELECT DISTINCT ?name ?date ?nDirector WHERE {
  SERVICE wikibase:label { bd:serviceParam wikibase:language "en_US". }

  {ITEM} wdt:P57 ?director .
  {ITEM} wdt:P577 ?date .
  ?director rdfs:label ?nDirector .
  filter(lang(?nDirector) = "en") .

  {ITEM} rdfs:label ?name .
  filter(lang(?name) = "en") .
}
"""


def query(entity: str) -> list[Card]:
    assert "{ITEM}" in QUERY
    results = get_results(QUERY.replace("{ITEM}", entity))
    if len(results) == 0:
        return []
    if len(results) > 1:
        results = sorted(results, key=lambda r: int(r["date"][:4]))
    return [
        Card(
            id=f"director-{entity[3:]}",
            front=f"What was the name of the director of the {results[0]['date'][:4]} film {results[0]['name']}?",
            back=results[0]["nDirector"],
        )
    ]
