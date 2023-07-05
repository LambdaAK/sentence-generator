from dataclasses import dataclass
from enum import Enum
import json




class Base:
    nouns_dict: dict[str, dict[str, str]] = {}
    adjectives: list[str] = []
    verbs_dict: dict[str, dict[str, str]] = {}

    def __init__(self):
        with open('./nouns.json', 'r') as f:
            self.nouns_dict = json.load(f)

        # read the adjectives
        with open('./adjectives.json', 'r') as f:
            self.adjectives = json.load(f)

        with open('./verbs.json', 'r') as f:
            self.verbs_dict = json.load(f)



class Plurality(Enum):
    SINGULAR = 1
    PLURAL = 2

class Article(Enum):
    DEFINITE = 1
    INDEFINITE = 2


class Tense(Enum):
    INFINITIVE = 1
    PAST_TENSE = 2
    PAST_PARTICIPLE = 3
    PRESENT_PARTICIPLE = 4
    THIRD_PERSON_SINGULAR = 5


@dataclass
class Noun(Base):
    plurality: Plurality
    word: str

    def __repr__(self):
        super().__init__()
        # if it's plural, add as 's' or 'es'
        match self.plurality:
            case Plurality.SINGULAR:
                return self.word
            case Plurality.PLURAL:
                return self.nouns_dict[self.word]["plural"]
        

@dataclass
class Adjective:
    word: str

    def __repr__(self) -> str:
        return self.word
    


class Verb(Base):
    def __init__(self):
        super().__init__()


@dataclass
class StandardVerb(Verb):
    word: str
    tense: Tense

    def to_string(self, plurality: Plurality) -> str:
        super().__init__()
        match self.tense:
            case Tense.INFINITIVE:
                return self.word
            case Tense.PAST_TENSE:
                return self.verbs_dict[self.word]["past"]
            case _:
                raise NotImplementedError("This tense is not implemented yet")
            

@dataclass
class PastParticipleVerb(Verb):
    word: str

    def to_string(self, plurality: Plurality) -> str:
        super().__init__()
        verb_form = self.verbs_dict[self.word]["past participle"]
        match plurality:
            case Plurality.SINGULAR:
                return f"has {verb_form}"
            case Plurality.PLURAL:
                return f"have {verb_form}"
    
@dataclass
class PresentParticipleVerbPresent(Verb):
    word: str

    def to_string(self, plurality: Plurality) -> str:
        super().__init__()
        verb_form = self.verbs_dict[self.word]["present participle"]
        match plurality:
            case Plurality.SINGULAR:
                return f"is {verb_form}"
            case Plurality.PLURAL:
                return f"are {verb_form}"
            

@dataclass
class PresentParticipleVerbPast(Verb):
    word: str

    def to_string(self, plurality: Plurality) -> str:
        super().__init__()
        verb_form = self.verbs_dict[self.word]["present participle"]
        match plurality:
            case Plurality.SINGULAR:
                return f"was {verb_form}"
            case Plurality.PLURAL:
                return f"were {verb_form}"
            

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
    
@dataclass
class Sentence():
    noun_phrase: NounPhrase
    verb: Verb

    def __repr__(self) -> str:
        return f'{self.noun_phrase} {self.verb.to_string(self.noun_phrase.noun.plurality)}'
