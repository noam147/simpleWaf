import re
from enum import Enum
from dataclasses import dataclass
from typing import List

MAX_SQLI_SCORE = 2

# the options for the sqli-defender strictness
class SqliStrictness(Enum):
    LOW = 0 # no defense
    MID = 1 # specific
    STRICT = 2


@dataclass
class SqliRule:
    regex: str
    weight: float # how much effect finding this regex has
    strictness: SqliStrictness

SQLI_REGEX: List[SqliRule] = [
    SqliRule(r"(?i)\b(?:OR|AND)\b\s+((.*?)=(.*?)|TRUE|FALSE|NULL)", \
             2.0, SqliStrictness.MID),
    SqliRule(r"(?i)\bUNION\b.*\bSELECT\b", 2.0, SqliStrictness.MID),
    SqliRule(r";.*--", 1.0, SqliStrictness.STRICT),
    SqliRule(r"(?i)\b(SLEEP|BENCHMARK)\b\s*\(.*\)", 2.0, SqliStrictness.MID),
    SqliRule(r"(?i)--\s*$", 1.0, SqliStrictness.STRICT),
    SqliRule(r"(?i)\b(exec)", 1.0, SqliStrictness.STRICT),
    SqliRule(r"(?i)\b(xp_regraded)", 1.0, SqliStrictness.STRICT),
    SqliRule(r"(?i)\b(waitfor)", 1.0, SqliStrictness.STRICT),
    SqliRule(r"(?i)\b(delay)", 1.0, SqliStrictness.STRICT),
]



def find_sqli(data: str, strictness: SqliStrictness = SqliStrictness.STRICT, banned_characters: str = '') -> bool:
        score = 0
        # search for sqli using the regular-expressions in the data given
        for pattern in SQLI_REGEX:
            # check only the regex with a valid strictness
            if pattern.strictness.value <= strictness.value:
                if re.search(pattern.regex, data):
                   # print(pattern) # debugging and testing
                    score += pattern.weight

        if banned_characters !=  '':
            # search for invalid characters
            banned_characters_regex = f"(?i)[{banned_characters}]"
            if re.search(banned_characters_regex, data):
                return True

        return score >= MAX_SQLI_SCORE
