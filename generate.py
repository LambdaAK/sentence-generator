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

    _adjectives: list[Adjective] = (generate_adjective() for _ in range(random.randint(0, 3)))
    adjectives: list[Adjective] = []

    [adjectives.append(a) for a in _adjectives if a not in adjectives]

    # decide whether to make it a noun phrase with an article or not
    if random.choice([True, False]):
        return NounPhraseWithArticle(random.choice([Article.DEFINITE, Article.INDEFINITE]), generate_noun(), adjectives)
    else:
        return NounPhraseWithoutArticle(generate_noun(), adjectives)
