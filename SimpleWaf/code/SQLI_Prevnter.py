
from Attack_Preventer import Attack_Scanner
from tornado.httputil import HTTPServerRequest
from copy import deepcopy
class SQLI_Preventer(Attack_Scanner):
    @staticmethod
    def replace_sql(text:str) -> str:
        # result in chars that do not have the affect of ' in sql terms
        text = text.replace("\"","&quot;")
        text = text.replace("'","&#x27")
        return text
    @staticmethod
    def edit_request(request: HTTPServerRequest) -> HTTPServerRequest:
        new_request = deepcopy(request)
        new_request.uri = SQLI_Preventer.replace_sql(new_request.uri)
        new_headers = {}
        for key,val in request.headers.items():
            new_headers[key] = SQLI_Preventer.replace_sql(val)
        new_request.headers = new_headers
        if new_request.body and isinstance(request.body, str):#if data isn't str, we do not need to check it
            new_request.data = SQLI_Preventer.replace_sql(new_request.body)
        return new_request
