from __future__ import annotations

from dataclasses import dataclass
from hashlib import new as hasher
from json import JSONDecodeError, loads
from pathlib import Path
from sys import exit
from time import sleep
from urllib.parse import quote
from typing import Optional

from requests import get

DELAY = 10
URL = "https://query.wikidata.org/bigdata/namespace/wdq/sparql?query="
HEADERS = {
    "User-Agent": "AnkiWikidata/0.0 (https://github.com/langston-barrett/anki-wikidata; langston.barrett@gmail.com)"
}


def query_url(query: str, /) -> str:
    return URL + quote(query)


def cache_key(query: str, /) -> str:
    h = hasher("sha256")
    h.update(query.encode("utf-8"))
    return h.hexdigest()


def cache_path(query: str, cache: Path) -> Path:
    return cache / cache_key(query)


def run_query(
    query: str, /, *, delay: int = DELAY, cache: Optional[Path] = None
) -> str:
    if cache is not None:
        cached = cache_path(query, cache)
        if cached.exists():
            return cached.read_text()

    sleep(delay)
    result = get(query_url(query), params={"format": "json"}, headers=HEADERS).text

    if cache is not None:
        cached = cache_path(query, cache)
        cached.write_text(result)

    return result


def get_results(
    query: str, /, *, delay: int = DELAY, cache: Optional[Path] = Path(".cache")
) -> list[dict[str, str]]:
    if cache is not None:
        cache.mkdir(mode=0o750, parents=True, exist_ok=True)

    result_text = run_query(query, delay=delay, cache=cache)
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
