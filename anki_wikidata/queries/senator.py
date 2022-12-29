from __future__ import annotations

from queries.util import get_results

from ..card import Card

QUERY = """
SELECT DISTINCT ?name ?nState WHERE {
  SERVICE wikibase:label { bd:serviceParam wikibase:language "en_US". }

  {ITEM} p:P39 ?statement .  # position held statement
  ?statement pq:P768 ?district .  # electoral district qualifier
  ?district wdt:P31/wdt:P279 wd:Q58425000 .  # instance of subclass of senate constituency
  ?district wdt:P131 ?state .  # located in
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
            id=f"governor-{entity[3:]}",
            front=f"{results[0]['name']} was senator of what state?",
            back=results[0]["nState"],
        )
    ]
