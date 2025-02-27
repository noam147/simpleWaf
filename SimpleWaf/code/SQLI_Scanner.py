import requests
from tornado.httputil import HTTPServerRequest
from Attack_Scanner import IAttack_Scanner
from SQLI_Scanner_Utils import find_sqli, SqliStrictness

class SqliScanner(IAttack_Scanner):
    @staticmethod
    def scan(data: HTTPServerRequest,pref_of_web) -> bool:

        if isinstance(pref_of_web, int):
            strictness = (SqliStrictness.LOW if pref_of_web == 0 else
                           SqliStrictness.MID if pref_of_web == 1
                           else SqliStrictness.STRICT)

        else:
            print("error on sql scanner. check type of pref")
            strictness = SqliStrictness.STRICT

        blocked_characters = ''
        if find_sqli(data.uri, strictness, blocked_characters):
            return True
        for k,v in data.headers.items():
            if find_sqli(v, strictness, blocked_characters):
                return True
        if find_sqli(data.body.decode("utf-8"), strictness, blocked_characters):
            return True
        #if the json isn't dict - do not check it
        if isinstance(data.body, dict):
            for k,v in data.body.items():
                if find_sqli(v, strictness, blocked_characters):
                    return True
        return False