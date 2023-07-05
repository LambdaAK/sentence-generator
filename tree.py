from dataclasses import dataclass
from enum import Enum
import json


nouns_dict: dict[str, dict[str, str]] = {}
adjectives: list[str] = []

with open('./nouns.json', 'r') as f:
    nouns_dict = json.load(f)

# read the adjectives
with open('./adjectives.json', 'r') as f:
    adjectives = json.load(f)



class Plurality(Enum):
    SINGULAR = 1
    PLURAL = 2

class Article(Enum):
    DEFINITE = 1
    INDEFINITE = 2


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


class NounPhraseAdjectiveLevel:
    pass


@dataclass
class NounPhraseWithoutArticle(NounPhrase):
    noun: NounPhraseAdjectiveLevel

    def __repr__(self) -> str:
        return self.noun.__repr__()
    
@dataclass
class NounPhraseWithArticle(NounPhrase):
    article: Article
    noun_phrase_adjective_level: NounPhraseAdjectiveLevel

    def __repr__(self) -> str:
        article_string = ""
        match self.article, self.noun_phrase_adjective_level.noun.plurality:
            case Article.DEFINITE, _:
                article_string = "the"
            case Article.INDEFINITE, Plurality.SINGULAR:
                # if the noun starts with a vowel, use 'an' instead of 'a'
                if self.noun_phrase_adjective_level.noun.noun[0] in ['a', 'e', 'i', 'o', 'u']:
                    article_string = "an"
                else:
                    article_string = "a"

            case Article.INDEFINITE, Plurality.PLURAL:
                article_string = "some"

        return f'{article_string} {self.noun_phrase_adjective_level}'


@dataclass
class NounPhraseWithAdjective(NounPhraseAdjectiveLevel):
    adjective: Adjective
    noun: Noun

    def __repr__(self) -> str:
        return f'{self.adjective} {self.noun}'

@dataclass
class NounPhraseWithoutAdjective(NounPhraseAdjectiveLevel):
    noun: Noun

    def __repr__(self) -> str:
        return self.noun.__repr__()