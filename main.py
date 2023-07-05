from enum import Enum
import json
from dataclasses import dataclass
from tree import *
from generate import *

phrases = list((generate_noun_phrase() for _ in range(100)))

for phrase in phrases:
    print(phrase)

