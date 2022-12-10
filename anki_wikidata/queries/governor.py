from __future__ import annotations

from queries.util import get_results

from ..card import Card

QUERY = """
SELECT DISTINCT ?name ?nState WHERE {
  SERVICE wikibase:label { bd:serviceParam wikibase:language "en_US". }

  {ITEM} wdt:P39 ?office .  # position held
  ?office wdt:P279+ wd:Q889821 .  # subclass of governor
  ?office wdt:P1001 ?state .  # jurisdiction
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
            id=f"governor-{entity}",
            front=f"{results[0]['name']} was governor of what state?",
            back=results[0]["nState"],
        )
    ]
