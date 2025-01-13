
import re
from enum import Enum
from dataclasses import dataclass
from typing import List, Type

SQL_INJECTION_CODE = 0
COMMAND_INJECTION_LINUX_CODE = 1
COMMAND_INJECTION_WINDOWS_CODE = 2

"""this class will have sqli and command injection"""
MAX_ATTACK_SCORE = 2
class StrictnessLevel(Enum):
    LOW = 0  # no defense
    MID = 1  # specific
    STRICT = 2

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
    SqliRule(r"(?i)\b(delay)", 1.0, StrictnessLevel.STRICT),
]

### for linux os ###
COMMAND_INJECTION_LINUX_REGEX: List[CommandInjectionRule] = [
    CommandInjectionRule(r"(?i)\b(?:sudo|rm|mv|/etc/|cp|wget|curl|chmod|chown|kill|shutdown|reboot|service|iptables)\b", 2.0,StrictnessLevel.STRICT),
    CommandInjectionRule(r";|&&|\|\|", 1.5, StrictnessLevel.MID),
    CommandInjectionRule(r"(<|>|>>|2>&1)", 1.0, StrictnessLevel.MID),
    CommandInjectionRule(r"&\s*$", 1.5, StrictnessLevel.STRICT),
    CommandInjectionRule(r"(?i)\b(base64|eval|exec|system|popen|shell_exec|open)\b", 2.0, StrictnessLevel.STRICT),
    CommandInjectionRule(r"(?i)\b(/etc/passwd|/etc/shadow|/var/log|/root)\b", 2.5, StrictnessLevel.MID),
]
### for windows os ###
COMMAND_INJECTION_WINDOWS_REGEX: List[CommandInjectionRule] = [
    CommandInjectionRule(r"(?i)\b(?:dir|del|ipconfig|netstat|tasklist|shutdown|cls|whoami|set|reg)\b", 2.0,StrictnessLevel.STRICT),
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

def find_command_injection_windows(data: str, strictness: StrictnessLevel = StrictnessLevel.STRICT, banned_characters: str = '')->bool:
    return find_attack(COMMAND_INJECTION_WINDOWS_CODE,data,strictness,banned_characters)
def find_command_injection_linux(data: str, strictness: StrictnessLevel = StrictnessLevel.STRICT, banned_characters: str = '')->bool:
    return find_attack(COMMAND_INJECTION_LINUX_CODE,data,strictness,banned_characters)
def find_sqli(data: str, strictness: StrictnessLevel = StrictnessLevel.STRICT, banned_characters: str = '')->bool:
    return find_attack(SQL_INJECTION_CODE,data,strictness,banned_characters)

def find_attack(attack_code:int,data: str, strictness: StrictnessLevel = StrictnessLevel.STRICT, banned_characters: str = '') -> bool:
    """attack code - code for attack to scan"""

    attack_regex: list[AttackRule] = []

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

    if banned_characters != '':
        # search for invalid characters
        banned_characters_regex = f"(?i)[{banned_characters}]"
        if re.search(banned_characters_regex, data):
            return True

    return score >= MAX_ATTACK_SCORE
