import json

import requests
import tornado.escape
import tornado.httputil
# import sql checking
import sys

from DDOS_Scanner import DDOSScanner

# appending the directory of SQLI_Modules
sys.path.append('SQLI_Modules')
from SQLI_Scanner import SqliScanner  # Importing the SQLI scanning module

class SearchAttacks:
    def __init__(self, msg_from_client: tornado.httputil.HTTPServerRequest):
        self.current_request = msg_from_client

    def search_attacks(self) -> str:
        """
        Determines if a request contains attacks based on URL, headers, or body.
        :return: name of attack if an attack is detected (abort), empty string otherwise (pass through).
        """
        if self.__search_sql(self.current_request):
            return "SQL_INJECTION"
        if self.__search_ddos(self.current_request):
            return "DDOS"
        return ""


        # Check URL
        if self.__search_in_url(self.current_request.uri):
            return True

        # Check Headers
        headers_dict = dict(self.current_request.headers)
        if self.__search_in_headers(headers_dict):
            return True

        # Check JSON Body
        try:
            body = self.current_request.body
            if body:
                json_data = tornado.escape.json_decode(body)
                str_json = json.dumps(json_data)
                if self.__search_in_json(str_json):
                    return True
        except json.JSONDecodeError:
            print("Request does not contain valid JSON.")

        return False

    def __search_in_url(self, url: str) -> bool:
        """
        Search for SQL injections or other attacks in the URL.
        """
        return self.__search_sql(url)

    def __search_in_headers(self, dict_headers: dict) -> bool:
        """
        Search for SQL injections or other attacks in headers.
        """
        for key, value in dict_headers.items():
            if self.__search_sql(value):
                return True
        return False

    def __search_in_json(self, str_json: str) -> bool:
        """
        Search for SQL injections or other attacks in JSON data.
        """
        return self.__search_sql(str_json)

    def __search_sql(self, data: tornado.httputil.HTTPServerRequest) -> bool:
        """
        Check if the provided data contains SQL injections.
        """
        result = SqliScanner.scan(data)
        return result
    def __search_ddos(self,data: tornado.httputil.HTTPServerRequest) -> bool:
        return DDOSScanner.scan(data)
