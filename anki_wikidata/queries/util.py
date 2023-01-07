from __future__ import annotations

from dataclasses import dataclass
from json import JSONDecodeError, loads
from sys import exit
from time import sleep
from urllib.parse import quote

from requests import get

URL = "https://query.wikidata.org/bigdata/namespace/wdq/sparql?query="


def query_url(query: str) -> str:
    return URL + quote(query)


def run_query(query: str, delay: int = 1) -> str:
    sleep(delay)
    return get(query_url(query), params={"format": "json"}).text


def get_results(query: str, delay: int = 1) -> list[dict[str, str]]:
    result_text = run_query(query, delay=delay)
    try:
        return [
            {bind: val["value"] for (bind, val) in d.items()}
            for d in loads(result_text)["results"]["bindings"]
        ]
    except JSONDecodeError as e:
        print("Couldn't decode response:")
        print(result_text)
        print(e)
        exit(1)
