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
    word: str

    def __repr__(self):
        # if it's plural, add as 's' or 'es'
        match self.plurality:
            case Plurality.SINGULAR:
                return self.word
            case Plurality.PLURAL:
                return nouns_dict[self.word]["plural"]
        

@dataclass
class Adjective:
    word: str

    def __repr__(self) -> str:
        return self.word


'''
abstract class that represents a noun phrase
'''
class NounPhrase:
    pass


@dataclass
class NounPhraseWithoutArticle(NounPhrase):
    noun: Noun
    adjectives: list[Adjective]

    def __repr__(self) -> str:
        adjectives_string: str = ', '.join(
            list(
                map(
                    lambda x: x.word,
                    self.adjectives
                )
            )
        )
        return f'{adjectives_string} {self.noun}'
    
@dataclass
class NounPhraseWithArticle(NounPhrase):
    article: Article
    noun: Noun
    adjectives: list[Adjective]

    def __repr__(self) -> str:
        article_string = ""
        match self.article, self.noun.plurality:
            case Article.DEFINITE, _:
                article_string = "the"
            case Article.INDEFINITE, Plurality.SINGULAR:
                
                first_word = None

                # get the first adjective if possible, or the noun
                if len(self.adjectives) > 0:
                    first_word = self.adjectives[0].word
                else:
                    first_word = self.noun.word

                # if the first word starts with a vowel, use 'an'
                if first_word[0] in ['a', 'e', 'i', 'o', 'u']:
                    article_string = "an"
                else:
                    article_string = "a"
                
            case Article.INDEFINITE, Plurality.PLURAL:
                article_string = "some"

        adjectives_string: str = ', '.join(
            list(
                map(
                    lambda x: x.word,
                    self.adjectives
                )
            )
        )            

        return f'{article_string} {adjectives_string} {self.noun}'