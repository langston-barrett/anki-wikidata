#!/usr/bin/env python3

from __future__ import annotations

from json import dumps as json_dumps
from pathlib import Path
from sys import exit
from typing import List, Optional

import typer
import yaml
from pydantic import ValidationError

from anki_wikidata.card import Card
from anki_wikidata.conf import Config, Entity
from anki_wikidata.gen import write_deck
from anki_wikidata.queries import (
    begin_year,
    birth_country,
    birth_state,
    borough,
    brother,
    cabinet_position,
    death_year,
    director,
    election_winner,
    end_year,
    father,
    killed_by,
    governor,
    happened_year,
    location_state,
    manner_of_death,
    part_of_war,
    place_of_death,
    mother,
    political_party,
    president_during,
    publication_date,
    senator,
    spouse,
)
from anki_wikidata.queries.util import get_results

app = typer.Typer()


# TODO:
# - City of death
# - Sister
QUERIES = {
    "begin-year": begin_year.query,
    "birth-country": birth_country.query,
    "birth-state": birth_state.query,
    "borough": borough.query,
    "brother": brother.query,
    "cabinet-position": cabinet_position.query,
    "death-year": death_year.query,
    "director": director.query,
    "election-winner": election_winner.query,
    "end-year": end_year.query,
    "father": father.query,
    "killed-by": killed_by.query,
    "governor-of": governor.query,
    "happened-year": happened_year.query,
    "location-state": location_state.query,
    "manner-of-death": manner_of_death.query,
    "part-of-war": part_of_war.query,
    "place-of-death": place_of_death.query,
    "mother": mother.query,
    "political-party": political_party.query,
    "president-during": president_during.query,
    "publication-date": publication_date.query,
    "senator-of": senator.query,
    "spouse": spouse.query,
}


def dump_config(
    config: Config, config_file: Path, /, *, json: bool = False, normalize: bool = True
) -> None:
    # TODO: Normalize key order
    # https://stackoverflow.com/questions/18405537
    d = config.dict()
    if normalize:
        config.entities = sorted(config.entities, key=lambda e: e.name or "")
        d = config.dict()

    with open(config_file, mode="w") as f:
        if json:
            dumped = json_dumps(d, indent=2)
        else:
            dumped = yaml.dump(d)
        f.write(dumped)


def load_config_file(config_file: Path, /, *, create: bool = False) -> str:
    if not config_file.exists():
        if not create:
            print("No configuration file at", config_file)
            exit(1)
        dump_config(Config(entities=[]), config_file)
    return config_file.read_text()


def load_config(config_file: Path, /, *, create: bool = False) -> Config:
    config_dict = yaml.safe_load(load_config_file(config_file, create=create))
    if config_dict is None:
        print("Invalid YAML at", config_file)
        exit(1)
    try:
        return Config(**config_dict)
    except ValidationError as e:
        print(e.json())
        exit(1)


def choose_id(name: str, /, *, filter: Optional[str] = None) -> Optional[str]:
    results = ids(name)
    if results == []:
        print("No results")
        return None

    filtered_results = []
    if filter is None:
        filtered_results = results
    else:
        for (idx, (id, desc)) in enumerate(results):
            if filter in desc:
                filtered_results.append((id, desc))

    if len(filtered_results) == 0:
        return None
    if len(filtered_results) == 1:
        return filtered_results[0][0]

    for (idx, (_id, desc)) in enumerate(filtered_results):
        print(str(idx) + ":", desc)
    while True:
        try:
            user_idx = int(input("Choose a number: "))
        except ValueError:
            print("Not a number!")
            continue
        if user_idx >= len(results):
            print("Invalid choice!")
        else:
            break

    return results[idx][0]


@app.command()
def add(
    config_file: Path,
    entity: List[str] = [],
    name: Optional[str] = None,
    tag: List[str] = [],
    card: List[str] = [],
    filter: Optional[str] = None,
) -> None:
    """Add an entity to a deck"""
    config = load_config(config_file, create=False)

    if entity == [] or name != None:
        if name == None:
            name = input("Enter a name: ")
        entity_id = choose_id(name, filter=filter)
        if entity_id is None:
            return
        entity = [entity_id]

    for e in entity:
        if not e.startswith("Q"):
            print(
                f"'{e}' doesn't start with Q. Are you sure that's a Wikidata entity ID?"
            )
            exit(1)
        if any(e2.id == e for e2 in config.entities):
            print(f"{e} already in configuration file {config_file}")
            exit(1)
        config.entities.append(Entity(id=e, cards=card, tags=tag, name=name))
    dump_config(config, config_file, json=config_file.suffix == ".json")


@app.command()
def build(
    config_file: Path,
    output: Path = Path("out.apkg"),
    name: str = "default",
) -> None:
    """Build an apkg file from a deck (yml) file"""
    config = load_config(config_file)
    cards: List[Card] = []
    for entity in config.entities:
        for q in entity.cards:
            if q not in QUERIES:
                print("Invalid card name:", q)
                exit(1)
            cs = QUERIES[q]("wd:" + entity.id)
            if cs == []:
                print(f"Warning: No cards for {q}-{entity.id}")
            for c in cs:
                c.tags = entity.tags
                print(c.front, c.back)
                cards.append(c)
    for r in config.relations:
        print(r)
    write_deck(config.id, output, name, cards)


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


def ids(name: str, delay: int = 0) -> List[Tuple[str, str]]:
    """List IDs and descriptions Wikidata entities with a given name"""
    query = ID_QUERY.replace("{NAME}", name)
    results = get_results(query, delay=delay)
    return [(result["entity"].split("/")[-1], result["desc"]) for result in results]


@app.command()
def id(name: str) -> None:
    """List IDs and descriptions Wikidata entities with a given name"""
    # TODO use ids
    query = ID_QUERY.replace("{NAME}", name)
    results = get_results(query)
    for result in results:
        iden = result["entity"].split("/")[-1]
        print(iden + ":", result["desc"])


if __name__ == "__main__":
    app()
