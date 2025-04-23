import json

import requests
import tornado.escape
import tornado.httputil
# import sql checking
import sys
from Preferences_Items import Preferences_Items
from DDOS_Scanner import DDOSScanner
from File_Attack_Scanner import Files_Scanner
from Command_Injection_Scanner import CommandInjectionScanner

# appending the directory of SQLI_Modules
sys.path.append('SQLI_Modules')
from SQLI_Scanner import SqliScanner  # Importing the SQLI scanning module

class SearchAttacks:
    def __init__(self, msg_from_client: tornado.httputil.HTTPServerRequest):
        self.current_request = msg_from_client

    def search_attacks(self,prefs_of_web:Preferences_Items) -> str:
        """
        Determines if a request contains attacks based on URL, headers, or body.
        :return: name of attack if an attack is detected (abort), empty string otherwise (pass through).
        """
        if self.__search_sql(self.current_request, prefs_of_web.sql_level):
            return "SQL_INJECTION"
        elif self.__search_ddos(self.current_request,1):
            return "DDOS"
        if self.__search_files(self.current_request,prefs_of_web.file_attack_level):
            return "FILE_UPLOAD"
        elif self.__search_command_injection(self.current_request,(prefs_of_web.os_level,1)):#todo add field of restriction to command injeciton
            return "COMMAND_INJECTION"
        return ""

    def __search_sql(self, data: tornado.httputil.HTTPServerRequest, pref) -> bool:
        """
        Check if the provided data contains SQL injections.
        """
        result = SqliScanner.scan(data, pref)
        return result
    def __search_ddos(self,data: tornado.httputil.HTTPServerRequest, pref) -> bool:
        return DDOSScanner.scan(data, pref)

    def __search_files(self,data: tornado.httputil.HTTPServerRequest, pref) -> bool:
        return Files_Scanner.scan(data, pref)

    def __search_command_injection(self,data: tornado.httputil.HTTPServerRequest, pref) -> bool:
        return CommandInjectionScanner.scan(data, pref)


