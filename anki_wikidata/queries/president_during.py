from __future__ import annotations

from queries.util import get_results

from ..card import Card

QUERY = """
SELECT DISTINCT ?name ?nPresident WHERE {
  SERVICE wikibase:label { bd:serviceParam wikibase:language "en_US". }

  {ITEM} wdt:P585 ?date .

  ?president wdt:P31 wd:Q5 ; p:P39 ?statement.
  ?statement ps:P39 wd:Q11696 ; pq:P580 ?start. 

  OPTIONAL{ ?statement pq:P582 ?end. }
  BIND(IF(!BOUND(?end), NOW(), ?end) AS ?end)

  FILTER(?start <= ?date && ?date <= ?end)

  ?president rdfs:label ?nPresident .
  filter(lang(?nPresident) = "en") .

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
            id=f"president-during-{entity[3:]}",
            front=f"Who was US president during the {results[0]['name']}?",
            back=results[0]["nPresident"],
        )
    ]
