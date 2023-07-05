# grammar
noun_phrase ::= noun_phrase_with_article | noun_phrase_without_article

noun_phrase_with_article ::= article [adjective]* noun
noun_phrase_without_article ::= [adjective]* noun

article ::= indefinite_article | definite_article

noun ::= "cat" | "dog" | ....

adjective ::= "big" | "small" | ....