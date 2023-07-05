import json
import random
from tree import *

nouns: list[str] = []
adjectives: list[str] = []

with open('./nouns.json', 'r') as f:
    nouns = list(json.load(f).keys())

# read the adjectives
with open('./adjectives.json', 'r') as f:
    adjectives = json.load(f)


def generate_noun() -> Noun:
    # pick a random noun
    noun = random.choice(nouns)
    # pick a random plurality
    plurality = random.choice([Plurality.SINGULAR, Plurality.PLURAL])
    return Noun(plurality, noun)

def generate_adjective() -> Adjective:
    adjective = random.choice(adjectives)
    return Adjective(adjective)


def generate_noun_phrase() -> NounPhrase:
    # decide whether to make it a noun phrase with an adjective or not
    if random.choice([True, False]):
        return NounPhraseWithAdjective(generate_adjective(), generate_noun())
    else:
        return NounPhraseWithoutAdjective(generate_noun())

