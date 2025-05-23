
from Attack_Preventer import Attack_Scanner
from tornado.httputil import HTTPServerRequest
from copy import deepcopy
class SQLI_Preventer(Attack_Scanner):
    @staticmethod
    def replace_sql(text:str) -> str:
        # result in chars that do not have the affect of ' in sql terms
        text = text.replace("\"","&quot;")
        text = text.replace("'","&#x27;")
        return text
    @staticmethod
    def edit_request(request: HTTPServerRequest,pref_of_web) -> HTTPServerRequest:
        if isinstance(pref_of_web,bool) and pref_of_web == True:
            return request
        request.uri = SQLI_Preventer.replace_sql(request.uri)
        new_headers = {}
        for key,val in request.headers.items():
            new_headers[key] = SQLI_Preventer.replace_sql(val)
        request.headers = new_headers
        if request.body and isinstance(request.body, str):#if data isn't str, we do not need to check it
            request.body = SQLI_Preventer.replace_sql(request.body)
        return request
