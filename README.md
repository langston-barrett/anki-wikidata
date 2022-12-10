# anki-wikidata

Easily create high-quality [Anki][anki] cards with data from [Wikidata][wikidata]!

Effective use of Anki is difficult and time-consuming. anki-wikidata helps you
create high-quality Anki cards with a minimum of effort.

## Workflow

Let's say you're learning about Pablo Picasso. To get started creating cards,
first find the Wikidata entity identifier corresponding to Picasso:

```sh
anki-wikidata id "Pablo Picasso"
```
```
Q5593: Spanish painter and sculptor (1881–1973)
Q92627252: photograph by Man Ray 224564
Q7121722: song of the proto punk group The Modern Lovers
...
```

Now, check what kinds of cards `anki-wikidata` can create for this kind of
entity (`Q5593`):

```sh
anki-wikidata list Q5593
```
```
birth-country:
- In what country was Pablo Picasso born?
- Spain
...
```

Create a deck file which includes this identifier:

```sh
anki-wikidata add --card birth-country deck.yml Q5593
```

This will create a file `deck.yml` like so:

```yaml
entities:
- id: Q5593
  cards:
  - birth-country
```

You can then pass this file to `anki-wikidata build`:

```sh
anki-wikidata build deck.yml
```

This will create a deck `out.apkg` containing the card you saw earlier:

- *Front*: In what country was Pablo Picasso born?
- *Back*: Spain

## Installation

```sh
git clone https://github.com/langston-barrett/anki-wikidata
cd anki-wikidata
pip install .
anki-wikidata --help
```

Or, run it without installing:

```sh
git clone https://github.com/langston-barrett/anki-wikidata
cd anki-wikidata
pip install -r requirements.txt
env PYTHONPATH=$PYTHONPATH:$PWD python3 anki_wikidata/main.py --help
```

## Effective use of Anki with anki-wikidata

[There][20-rules] [are][prompts] [many][rules] [guides][augmenting] on the
effective use of spaced repetition software. This section discusses some
common recommendations and how anki-wikidata helps to address them.

### Use concise prompts

A *prompt* is the front side of a card. Using concise prompts makes review
sessions shorter and makes it harder to "pattern match" (see below). The
prompts in `anki-wikidata` are hand-written, and are constructed with brevity
in mind.

### Use atomic prompts

"Atomic" cards express the smallest meaningful portion of an idea. With a non-
atomic card, you can waste time reviewing one part of a card that you remember
well because you forgot another part of the card.

The data model of Wikidata consists of subject-predicate-object triples. In
a sense, most of Wikidata consists of "atomic" facts, so it's easy to convert
this data into "atomic" cards. Again, the hand-written prompts in 
`anki-wikidata` are written with atomicity in mind.

### Use unambiguous prompts

Each prompt should have a single, unambiguously correct answer. "The USA" and
"Florida, Missouri" are both correct answers to the question "Where was Mark
Twain born?", so this is an ambiguous prompt. A better version might be "In
which US state was Mark Twain born?" The only correct answer is "Missouri".

The hand-written prompts in `anki-wikidata` were constructed to be unambiguous.

### Avoid pattern-matching

Cards with extraneous detail allow your brain to associate the details of a
card with the answer, rather than truly remembering the answer. For example,
if you have the cards "What was the date of birth of John Lewis?" and "When was
José Martí born?", your brain might associate the phrase "What was the date of
birth of" with the answer to the first, leading you to be unable to remember
the fact in other contexts. It would be better to have two cards with nearly
identical wording.

`anki-wikidata` solves this problem once and for all by using the exact same
wording on every prompt that asks the same question.

### Avoid orphans

TODO

### Encode from multiple angles

TODO

### Avoid non-facts

TODO

## Development

Install development tools with `pip install -r dev-requirements.txt`. Use
`black` and `isort` to format changes, and Mypy to typecheck them.

[20-rules]: http://super-memory.com/articles/20rules.htm
[anki]: https://apps.ankiweb.net/
[augmenting]: http://augmentingcognition.com/ltm.html
[prompts]: https://notes.andymatuschak.org/z42J1vxsMjhkdbrqVfoqjiEesSzfaEqurBtoJ
[rules]: https://controlaltbackspace.org/precise/
[wikidata]: https://www.wikidata.org/wiki/Wikidata:Main_Page
