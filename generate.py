import json
import random
from tree import *

nouns: list[str] = []
adjectives: list[str] = []
verbs_dict: dict[str, dict[str, str]] = {}

with open('./nouns.json', 'r') as f:
    nouns = list(json.load(f).keys())

# read the adjectives
with open('./adjectives.json', 'r') as f:
    adjectives = json.load(f)

with open('./verbs.json', 'r') as f:
    verbs_dict = json.load(f)


def generate_noun() -> Noun:
    # pick a random noun
    noun = random.choice(nouns)
    # pick a random plurality
    plurality = random.choice([Plurality.SINGULAR, Plurality.PLURAL])
    return Noun(plurality, noun)

def generate_adjective() -> Adjective:
    adjective = random.choice(adjectives)
    return Adjective(adjective)

def generate_verb() -> Verb:
    # pick a random verb
    verb = random.choice(list(verbs_dict.keys()))
    # pick a random tense
    tense = random.choice([Tense.INFINITIVE, Tense.PAST_TENSE, Tense.PAST_PARTICIPLE, Tense.PRESENT_PARTICIPLE, Tense.THIRD_PERSON_SINGULAR])
    
    match tense:
        case Tense.INFINITIVE | Tense.THIRD_PERSON_SINGULAR:
            return StandardVerb(verb, Tense.INFINITIVE)
        case Tense.PAST_TENSE:
            return StandardVerb(verb, Tense.PAST_TENSE)
        case Tense.PAST_PARTICIPLE:
            return PastParticipleVerb(verb)
        case Tense.PRESENT_PARTICIPLE:
            if random.choice([True, False]):
                return PresentParticipleVerbPresent(verb)
            else:
                return PresentParticipleVerbPast(verb)
        

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
    

def generate_sentence() -> Sentence:
    noun_phrase: NounPhrase = generate_noun_phrase()
    verb: Verb = generate_verb()
    return Sentence(noun_phrase, verb)
