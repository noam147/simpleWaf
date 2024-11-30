import re

# the options for the sqli-defender strictness
class SQLI_STRICTNESS(enum):
    LOW = 0 # no defense
    MID = 1 # specific
    STRICT = 2

SQLI_REGEX = [
    (r"(?i)\b(?:OR|AND)\b\s+(\d+=\d+|TRUE|FALSE|NULL)",2, SQLI_STRICTNESS.MID),
     (r"(?i)\bUNION\b.*\bSELECT\b",2,SQLI_STRICTNESS.MID),
      (r";.*--",1,SQLI_STRICTNESS.MID),
       (r"(?i)\b(SLEEP|BENCHMARK)\b\s*\(.*\)",2,SQLI_STRICTNESS.MID),
        (r"(?i)--\s*$",1,SQLI_STRICTNESS.MID)]



def find_sqli(data: str) -> bool:
        score = 0
        for pattern in SQLI_REGEX:
            if re.search(pattern, data):
                score += 1
        return score > 2
