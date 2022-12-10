from __future__ import annotations

from json import loads
from urllib.parse import quote

from requests import get

URL = "https://query.wikidata.org/bigdata/namespace/wdq/sparql?query="


def query_url(query: str) -> str:
    return URL + quote(query)


def run_query(query: str) -> str:
    return get(query_url(query), params={"format": "json"}).text


def get_results(query: str) -> list[dict[str, str]]:
    return [
        {bind: val["value"] for (bind, val) in d.items()}
        for d in loads(run_query(query))["results"]["bindings"]
    ]
