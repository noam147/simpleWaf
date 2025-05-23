import re
from enum import Enum
from dataclasses import dataclass
from typing import List, Type
import urllib.parse

SQL_INJECTION_CODE = 0
COMMAND_INJECTION_LINUX_CODE = 1
COMMAND_INJECTION_WINDOWS_CODE = 2

"""this class will have sqli and command injection"""
MAX_ATTACK_SCORE = 2


class StrictnessLevel(Enum):
    LOW = 0  # no defense
    MID = 1  # specific
    STRICT = 2
def get_strictness_from_int(stric_int) -> StrictnessLevel:
    """use in attacks search, the default will be strict"""
    strictness = (StrictnessLevel.LOW if stric_int == 0 else
                  StrictnessLevel.MID if stric_int == 1
                  else StrictnessLevel.STRICT)
    return strictness

@dataclass
class AttackRule:
    regex: str
    weight: float
    strictness: StrictnessLevel


@dataclass
class SqliRule(AttackRule):
    pass


@dataclass
class CommandInjectionRule(AttackRule):
    pass


SQLI_REGEX: List[SqliRule] = [
    SqliRule(r"(?i)\b(?:OR|AND)\b\s+((.*?)=(.*?)|TRUE|FALSE|NULL)", 2.0, StrictnessLevel.MID),
    SqliRule(r"(?i)\bUNION\b.*\bSELECT\b", 2.0, StrictnessLevel.MID),
    SqliRule(r";.*--", 1.0, StrictnessLevel.STRICT),
    SqliRule(r"(?i)\b(SLEEP|BENCHMARK)\b\s*\(.*\)", 2.0, StrictnessLevel.MID),
    SqliRule(r"(?i)--\s*$", 1.0, StrictnessLevel.STRICT),
    SqliRule(r"(?i)\b(exec)", 1.0, StrictnessLevel.STRICT),
    SqliRule(r"(?i)\b(xp_regraded)", 1.0, StrictnessLevel.STRICT),
    SqliRule(r"(?i)\b(waitfor)", 1.0, StrictnessLevel.STRICT),
    SqliRule(r"(?i)\b(SELECT|INSERT|UPDATE|DELETE|DROP|ALTER|EXEC|MERGE|CALL)\b.*\bFROM\b", 1.0,
             StrictnessLevel.STRICT),
    SqliRule(r"(?i)\b(UNION|INTERSECT|MINUS|EXCEPT)\b\s*\b(ALL|DISTINCT)?\s*\bSELECT\b", 1.0, StrictnessLevel.MID),
    SqliRule(r"(?i)\b(CREATE|ALTER|DROP)\b\s+\b(TABLE|DATABASE|VIEW|FUNCTION|PROCEDURE)\b", 2.0,
             StrictnessLevel.STRICT),
    SqliRule(r"(?i)\b(INSERT|REPLACE)\b\s+INTO\b\s+[^\s]+\s+\(.*?\)\s*VALUES", 1.0, StrictnessLevel.MID),
    SqliRule(r"(?i)\b(pg_sleep)", 1.0, StrictnessLevel.STRICT),
    SqliRule(r"(?i)\b(select)*\b(into)", 1.0, StrictnessLevel.STRICT),
    SqliRule(r"(?i)\b(select).*\b(into)\s\b(temp)", 1.0, StrictnessLevel.STRICT),
    SqliRule(r"(?i)\b@\S*\s+\b(as)\s+\b(var|user|admin|password|username|main|email|gmail|temp)", 1.0,
             StrictnessLevel.STRICT),
    SqliRule(r"(?i)\b(exec)\s+\b(xp_cmdshell)", 1.0, StrictnessLevel.STRICT),
    SqliRule(r"(?i)\b(xp_cmdshell)", 1.0, StrictnessLevel.STRICT),
    SqliRule(r"(?i)\b(declare)\s+@.*", 1.0, StrictnessLevel.STRICT),
    SqliRule(
        r"(?i)\b(declare)\s+.*\s+\b(varchar|int|bigint|tinyint|smallint|real|decimal|numeric|char|string|str|chr|float|double|text|nvarchar|ntext|date|time|datetime|timestamp|datetime2|smalldatetime|datetimeoffset|bit|money|smallmoney|binary|image|varbinary)",
        1.0, StrictnessLevel.STRICT),
    SqliRule(r"(?i)\b(like)\s+'%.*", 2.0, StrictnessLevel.STRICT),
    SqliRule(r"(?i)\b(or)\s*.*(--|;|#)", 2.0, StrictnessLevel.STRICT),
    SqliRule(r"(?i)\b(group)\s+\b(by)\s+.*\b(having|where)\s*(.*?)(\s*?)=(\s*?)(.*?)", 1.0, StrictnessLevel.MID),
    SqliRule(r"(?i)\b(or)\s+(.*?)\s+\b(between)\s+(.*?)\s+\b(and)\s+(.*?)", 1.0, StrictnessLevel.MID),
]

### for linux os ###
COMMAND_INJECTION_LINUX_REGEX: List[CommandInjectionRule] = [
    CommandInjectionRule(r"(?i)\b(?:sudo|rm|mv|/etc/|cp|wget|curl|chmod|chown|kill|shutdown|reboot|service|iptables)\b",
                         2.0, StrictnessLevel.STRICT),
    CommandInjectionRule(r";|&&|\|\|", 1.5, StrictnessLevel.MID),
    CommandInjectionRule(r"(<|>|>>|2>&1)", 1.0, StrictnessLevel.MID),
    CommandInjectionRule(r"&\s*$", 1.5, StrictnessLevel.STRICT),
    CommandInjectionRule(r"(?i)\b(base64|eval|exec|system|popen|shell_exec|open)\b", 2.0, StrictnessLevel.STRICT),
    CommandInjectionRule(r"(?i)\b(/etc/passwd|/etc/shadow|/var/log|/root)\b", 2.5, StrictnessLevel.MID),
]
### for windows os ###
COMMAND_INJECTION_WINDOWS_REGEX: List[CommandInjectionRule] = [
    CommandInjectionRule(r"(?i)\b(?:dir|del|ipconfig|netstat|tasklist|shutdown|cls|whoami|set|reg)\b", 2.0,
                         StrictnessLevel.STRICT),
    CommandInjectionRule(r"&|&&|\|", 1.5, StrictnessLevel.MID),
    CommandInjectionRule(r"(<|>|>>|2>&1)", 1.0, StrictnessLevel.MID),
    CommandInjectionRule(r"(?i)\b(?:powershell|Invoke-Expression|IEX|Write-Output|Set-Variable|Get-Process)\b", 2.5,
                         StrictnessLevel.MID),
    CommandInjectionRule(r"(?i)\b(?:cmd|cmd.exe|wscript|cscript|mshta|schtasks|wmic|vbs|vba)\b", 2.0,
                         StrictnessLevel.STRICT),
    CommandInjectionRule(r"(?i)\b(HKLM|HKCU|reg add|reg delete|reg query)\b", 2.0, StrictnessLevel.STRICT),
    CommandInjectionRule(r"(?i)\b(C:\\windows|C:\\users|C:\\temp|C:\\ProgramData|autoexec.bat|boot.ini)\b", 2.5,
                         StrictnessLevel.MID),
]


def find_command_injection_windows(data: str, strictness: StrictnessLevel = StrictnessLevel.STRICT,
                                   banned_characters: str = '') -> bool:
    return find_attack(COMMAND_INJECTION_WINDOWS_CODE, data, strictness, banned_characters)


def find_command_injection_linux(data: str, strictness: StrictnessLevel = StrictnessLevel.STRICT,
                                 banned_characters: str = '') -> bool:
    return find_attack(COMMAND_INJECTION_LINUX_CODE, data, strictness, banned_characters)


def find_sqli(data: str, strictness: StrictnessLevel = StrictnessLevel.STRICT, banned_characters: str = '') -> bool:
    return find_attack(SQL_INJECTION_CODE, data, strictness, banned_characters)


def find_attack(attack_code: int, data: str, strictness: StrictnessLevel = StrictnessLevel.STRICT,
                banned_characters: str = '') -> bool:
    """attack code - code for attack to scan"""

    ### parse the html chars (for exmple the %7C)
    data = urllib.parse.unquote(data)
    attack_regex: List[AttackRule] = []

    if attack_code == SQL_INJECTION_CODE:
        attack_regex = SQLI_REGEX
    elif attack_code == COMMAND_INJECTION_LINUX_CODE:
        attack_regex = COMMAND_INJECTION_LINUX_REGEX
    elif attack_code == COMMAND_INJECTION_WINDOWS_CODE:
        attack_regex = COMMAND_INJECTION_WINDOWS_REGEX

    score = 0

    # search for attack using the regular-expressions in the data given
    for pattern in attack_regex:
        # check only the regex with a valid strictness
        if pattern.strictness.value <= strictness.value:
            if re.search(pattern.regex, data.upper()):
                score += pattern.weight

                ### to not waste additional checking ###
                if score >= MAX_ATTACK_SCORE:
                    return True
    if banned_characters != '':
        # search for invalid characters
        banned_characters_regex = f"(?i)[{banned_characters}]"
        if re.search(banned_characters_regex, data):
            return True

    return score >= MAX_ATTACK_SCORE
