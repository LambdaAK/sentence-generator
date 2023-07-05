from enum import Enum
import json
from dataclasses import dataclass
from tree import *
from generate import *


l = list((generate_noun_phrase() for _ in range(10)))

for i in l:
    print(i)


