#!/usr/bin/env python3

from __future__ import annotations

from pathlib import Path
from sys import exit
from typing import List

import typer
import yaml
from pydantic import ValidationError

from anki_wikidata.conf import Config, Entity
from anki_wikidata.queries import birth_country
from anki_wikidata.queries.util import get_results

app = typer.Typer()


QUERIES = {
    "birth_country": birth_country.query,
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
def add(config_file: Path, entity: str, card: List[str] = []) -> None:
    if not entity.startswith("Q"):
        print(
            f"'{entity}' doesn't start with Q. Are you sure that's a Wikidata entity ID?"
        )
        exit(1)
    config = load_config(config_file, create=True)
    if any(e.id == entity for e in config.entities):
        print(f"{entity} already in configuration file {config_file}")
        exit(1)
    config.entities.append(Entity(id=entity, cards=card))
    dump_config(config, config_file)


@app.command()
def build(config_file: Path) -> None:
    config = load_config(config_file)
    for entity in config.entities:
        for query_name in entity.cards:
            print(QUERIES[query_name]("wd:" + entity.id))


@app.command()
def list(entity: str) -> None:
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
    query = ID_QUERY.replace("{NAME}", name)
    results = get_results(query)
    for result in results:
        iden = result["entity"].split("/")[-1]
        print(iden + ":", result["desc"])


if __name__ == "__main__":
    app()