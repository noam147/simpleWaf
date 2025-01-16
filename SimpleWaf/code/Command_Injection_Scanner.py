import requests
from tornado.httputil import HTTPServerRequest
from Attack_Scanner import IAttack_Scanner
from GenericAttackUtils import find_command_injection_windows,find_command_injection_linux,StrictnessLevel

class CommandInjectionScanner(IAttack_Scanner):
    @staticmethod
    def scan(data: HTTPServerRequest) -> bool:
        ### TO DO: need to check the web os ###

        # get info from db
        strictness = StrictnessLevel.STRICT
        blocked_characters = ''
        if find_command_injection_linux(data.uri, strictness, blocked_characters):
            return True
        for k,v in data.headers.items():
            if find_command_injection_linux(v, strictness, blocked_characters):
                return True
        if find_command_injection_linux(data.body.decode("utf-8"), strictness, blocked_characters):
            return True
        #if the json isn't dict - do not check it
        if isinstance(data.body, dict):
            for k,v in data.body.items():
                if find_command_injection_linux(v, strictness, blocked_characters):
                    return True

        return False