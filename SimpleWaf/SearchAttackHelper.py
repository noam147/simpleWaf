import requests
import json

#import sql chcking
import sys
# appending the directory of SQLI_Modules
sys.path.append('SQLI_Modules')
# now we can import mod
from SQLI_Scanner import SqliScanner
# calling the scan function of SqliScanner
#example of usage:
#result = SqliScanner.scan("hello")
#print("SQL injection result: "+str(result))
class SearchAttacks:

    def __init__(self,msg_from_client:requests.Request):
        self.current_request = msg_from_client
    def search_attacks(self) -> bool:
        """func will tell the waf if to pass a msg or abort
        :return - true: abort - there is an attack.
        false: there isn't an attack"""

        ###check url ###
        if self.__search_in_url(self.current_request.url):
            return True
        ###check headers ###
        headers_dict = dict(self.current_request.headers)
        if self.__search_in_headers(headers_dict):
            return True
        #str_headers = json.dumps(headers_dict)
        ##search in json (if request has one)
        try:
            json_dict = dict(self.current_request.json)
            str_json = json.dumps(json_dict)
            if self.__search_in_json(str_json):
                return True
        except Exception:
            pass#there is not a json part in here
        return False


        """"#sql:
        flag1 = self.__search_sql(self.current_request.url)
        flag2 = self.__search_sql(str_headers)
        flag3 = self.__search_sql(str_data)
        if flag1 or flag2 or flag3:
            return True"""

    def __search_in_url(self,url:str)->bool:
        if self.__search_sql(url):
            return True
        return False
    def __search_in_headers(self,dict_headers:dict)->bool:
        for key,value in dict_headers.items():
            if self.__search_sql(value):
                return True
        return False
    def __search_in_json(self,str_json):
        if self.__search_sql(data=str_json):
            return True
        return False



    def __search_sql(self, data:str) -> bool:
        # calling the scan function of SqliScanner
        # example of usage:
        result = SqliScanner.scan(data)
        print("SQL injection result: " + str(result))
        return result
