#!/usr/bin/env python3

from __future__ import annotations

from pathlib import Path
from sys import exit
from typing import List

import typer
import yaml
from pydantic import ValidationError

from anki_wikidata.conf import Config, Entity
from anki_wikidata.gen import write_deck
from anki_wikidata.queries import (
    birth_country,
    birth_state,
    borough,
    governor,
    political_party,
    senator,
)
from anki_wikidata.queries.util import get_results

app = typer.Typer()


QUERIES = {
    "birth-country": birth_country.query,
    "birth-state": birth_state.query,
    "borough": borough.query,
    "governor": governor.query,
    "senator": senator.query,
    "political-party": political_party.query,
}


def dump_config(config: Config, config_file: Path) -> None:
    with open(config_file, mode="w") as f:
        f.write(yaml.dump(config.dict()))


def load_config_file(config_file: Path, create: bool = False) -> str:
    if not config_file.exists():
        if not create:
            print("No configuration file at", config_file)
            exit(1)
        dump_config(Config(entities=[]), config_file)
    return config_file.read_text()


def load_config(config_file: Path, create: bool = False) -> Config:
    config_dict = yaml.safe_load(load_config_file(config_file, create=create))
    if config_dict is None:
        print("Invalid YAML at", config_file)
        exit(1)
    try:
        return Config(**config_dict)
    except ValidationError as e:
        print(e.json())
        exit(1)


@app.command()
def add(config_file: Path, entity: List[str], card: List[str] = []) -> None:
    """Add an entity to a deck"""
    config = load_config(config_file, create=True)
    for e in entity:
        if not e.startswith("Q"):
            print(
                f"'{e}' doesn't start with Q. Are you sure that's a Wikidata entity ID?"
            )
            exit(1)
        if any(e2.id == e for e2 in config.entities):
            print(f"{e} already in configuration file {config_file}")
            exit(1)
        config.entities.append(Entity(id=e, cards=card))
    dump_config(config, config_file)


@app.command()
def build(
    config_file: Path, output: Path = Path("out.apkg"), name: str = "default"
) -> None:
    """Build an apkg file from a deck (yml) file"""
    config = load_config(config_file)
    cards = []
    for entity in config.entities:
        for query_name in entity.cards:
            if query_name not in QUERIES:
                print("Invalid card name:", query_name)
                exit(1)
            cs = QUERIES[query_name]("wd:" + entity.id)
            for card in cs:
                print(card)
            cards.extend(cs)
    write_deck(output, name, cards)


@app.command()
def list(entity: str) -> None:
    """List cards for entity"""
    if not entity.startswith("Q"):
        print(
            f"'{entity}' doesn't start with Q. Are you sure that's a Wikidata entity ID?"
        )
        exit(1)
    for query_name, query in QUERIES.items():
        for card in query("wd:" + entity):
            print(query_name + ":")
            print("-", card.front)
            print("-", card.back)


@app.command()
def query(q: str) -> None:
    """Query Wikidata"""
    for result in get_results(q):
        print(result)


ID_QUERY = """
SELECT DISTINCT ?entity ?desc WHERE {
  SERVICE wikibase:label { bd:serviceParam wikibase:language "en_US". }
  ?entity rdfs:label '{NAME}'@en .
  ?entity schema:description ?desc .
  filter(lang(?desc) = "en") .
} 
"""


@app.command()
def id(name: str) -> None:
    """List IDs and descriptions Wikidata entities with a given name"""
    query = ID_QUERY.replace("{NAME}", name)
    results = get_results(query)
    for result in results:
        iden = result["entity"].split("/")[-1]
        print(iden + ":", result["desc"])


if __name__ == "__main__":
    app()
