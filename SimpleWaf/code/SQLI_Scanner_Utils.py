import re
from enum import Enum
from dataclasses import dataclass
from typing import List
from GenericAttackUtils import SQLI_REGEX
MAX_SQLI_SCORE = 2


# the options for the sqli-defender strictness
class SqliStrictness(Enum):
    LOW = 0  # no defense
    MID = 1  # specific
    STRICT = 2


@dataclass
class SqliRule:
    regex: str
    weight: float  # how much effect finding this regex has
    strictness: SqliStrictness


def find_sqli(data: str, strictness: SqliStrictness = SqliStrictness.STRICT, banned_characters: List[str] = '') -> bool:
    score = 0
    # search for sqli using the regular-expressions in the data given
    for pattern in SQLI_REGEX:
        # check only the regex with a valid strictness
        if pattern.strictness.value <= strictness.value:
            if re.search(pattern.regex, data.upper()):
                score += pattern.weight

    if len(banned_characters) > 0:
        # search for invalid characters
        banned_characters_regex = f"(?i)[{re.escape(''.join(banned_characters))}]"
        if re.search(banned_characters_regex, data):
            return True

    return score >= MAX_SQLI_SCORE
