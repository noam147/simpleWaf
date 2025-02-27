import requests
from tornado.httputil import HTTPServerRequest
from Attack_Scanner import IAttack_Scanner
from GenericAttackUtils import find_command_injection_windows,find_command_injection_linux,StrictnessLevel
from enum import Enum

class OS(Enum):
    LINUX = 0
    WINDOWS = 1
    OTHER_NOT_SUPPORT = 2
class CommandInjectionScanner(IAttack_Scanner):
    @staticmethod
    def scan(data: HTTPServerRequest, pref_of_web) -> bool:
        if isinstance(pref_of_web, tuple) and len(pref_of_web) == 2:
            int_stric,int_os_level = pref_of_web
            strictness = (StrictnessLevel.LOW if int_stric == 0 else
                          StrictnessLevel.MID if int_stric == 1
                          else StrictnessLevel.STRICT)
            os_system = (OS.LINUX if int_os_level == 0 else
                          OS.WINDOWS if int_os_level == 1
                          else OS.OTHER_NOT_SUPPORT)

        else:
            print("error on command injection. check type of pref")
            strictness = StrictnessLevel.STRICT
            os_system = OS.LINUX

        blocked_characters = ''
        if os_system == OS.LINUX:
            command_search_to_activate = find_command_injection_linux
        elif os_system == OS.WINDOWS:
            command_search_to_activate = find_command_injection_windows
        else:
            return False

        if command_search_to_activate(data.uri, strictness, blocked_characters):
            return True
        for k,v in data.headers.items():
            if command_search_to_activate(v, strictness, blocked_characters):
                return True

        if command_search_to_activate(data.body.decode("utf-8") if isinstance(data.body,bytes) else data.body, strictness, blocked_characters):
            return True
        #if the json isn't dict - do not check it
        if isinstance(data.body, dict):
            for k,v in data.body.items():
                if command_search_to_activate(v, strictness, blocked_characters):
                    return True

        return False