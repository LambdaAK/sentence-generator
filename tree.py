from dataclasses import dataclass
from enum import Enum
import json


nouns_dict: dict[str, list[str]] = {}
adjectives: list[str] = []

with open('./nouns.json', 'r') as f:
    nouns_dict = json.load(f)

# read the adjectives
with open('./adjectives.json', 'r') as f:
    adjectives = json.load(f)



class Plurality(Enum):
    SINGULAR = 1
    PLURAL = 2


@dataclass
class Noun:
    plurality: Plurality
    noun: str

    def __repr__(self):
        # if it's plural, add as 's' or 'es'
        match self.plurality:
            case Plurality.SINGULAR:
                return self.noun
            case Plurality.PLURAL:
                return nouns_dict[self.noun]["plural"]
        

@dataclass
class Adjective:
    adjective: str

    def __repr__(self) -> str:
        return self.adjective


'''
abstract class that represents a noun phrase
'''
class NounPhrase:
    pass


@dataclass
class NounPhraseWithAdjective(NounPhrase):
    adjective: Adjective
    noun: Noun

    def __repr__(self) -> str:
        return f'{self.adjective} {self.noun}'

@dataclass
class NounPhraseWithoutAdjective(NounPhrase):
    noun: Noun

    def __repr__(self) -> str:
        return self.noun.__repr__()