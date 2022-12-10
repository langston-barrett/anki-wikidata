#! /usr/bin/env nix-shell
#! nix-shell -i python3 -p python3 python3Packages.requests python3Packages.rich

from json import loads
from pathlib import Path
from sys import argv
from urllib.parse import quote

from requests import get
from rich.traceback import install

URL = "https://query.wikidata.org/bigdata/namespace/wdq/sparql?query="


def query_url(query):
    return URL + quote(query)


QUERY = """
SELECT DISTINCT ?nProp ?prop WHERE {
  SERVICE wikibase:label { bd:serviceParam wikibase:language "en_US". }
  {
    {ITEM} ?p ?o .
    ?prop wikibase:directClaim ?p .
    ?prop rdfs:label ?nProp .
    filter(lang(?nProp) = "en") .
  } UNION {
    ?o ?p {ITEM} .
    ?prop wikibase:directClaim ?p .
    ?prop rdfs:label ?nProp .
    filter(lang(?nProp) = "en") .
  }
  filter(lang(?nProp) = "en") .
}
LIMIT 200
"""


def run_query(query):
    return get(query_url(query), params={"format": "json"}).text


def main():
    if len(argv) != 2:
        print("Usage: ./props.py WIKIDATA_ENTITY_ID")
        return
    result = loads(run_query(QUERY.replace("{ITEM}", f"wd:{argv[1]}")))
    for d in result["results"]["bindings"]:
        print(d["prop"]["value"], d["nProp"]["value"])


if __name__ == "__main__":
    main()
