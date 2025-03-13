import requests
from tornado.httputil import HTTPServerRequest
from Attack_Scanner import IAttack_Scanner
#from SQLI_Scanner_Utils import find_sqli, SqliStrictness
from GenericAttackUtils import find_sqli,get_strictness_from_int,StrictnessLevel
class SqliScanner(IAttack_Scanner):
    @staticmethod
    def scan(data: HTTPServerRequest,pref_of_web) -> bool:

        if isinstance(pref_of_web, int):
            strictness = get_strictness_from_int(pref_of_web)
        else:
            print("error on sql scanner. check type of pref")
            strictness = StrictnessLevel.STRICT

        blocked_characters = ''
        if find_sqli(data.uri, strictness, blocked_characters):
            return True
        for k,v in data.headers.items():
            if find_sqli(v, strictness, blocked_characters):
                return True
        if find_sqli(data.body.decode("utf-8") if isinstance(data.body,bytes) else data.body, strictness, blocked_characters):
            return True
        #if the json isn't dict - do not check it
        if isinstance(data.body, dict):
            for k,v in data.body.items():
                if find_sqli(v, strictness, blocked_characters):
                    return True
        return False