from Attack_Scanner import IAttack_Scanner
from SQLI_Scanner_Utils import find_sqli,SqliStrictness

class SqliScanner(IAttack_Scanner):
    @staticmethod
    def scann(data: str):
        # get info from db
        strictness = SqliStrictness.STRICT
        blocked_characters = ''
        return find_sqli(data, strictness, blocked_characters)