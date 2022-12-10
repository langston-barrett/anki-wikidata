#!/usr/bin/env python3

from setuptools import find_packages, setup

with open("./README.md") as f:
    long_description = f.read()

with open("./requirements.txt") as f:
    requirements = list(f.read().splitlines())

setup(
    name="anki-wikidata",
    version="0.0.0",
    license="MIT",
    author="Langston Barrett",
    author_email="langston.barrett@gmail.com",
    description="Generate Anki cards with data from Wikidata",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/langston-barrett/anki-wikidata",
    project_urls={"Documentation": "https://github.com/langston-barrett/anki-wikidata"},
    packages=find_packages(),
    platforms="any",
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": ["anki-wikidata = anki_wikidata=main:app"],
    },
)
