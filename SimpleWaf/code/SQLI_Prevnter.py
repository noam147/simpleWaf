
from Attack_Preventer import Attack_Scanner
from requests import Request
class SQLI_Preventer(Attack_Scanner):
    @staticmethod
    def replace_sql(text:str) -> str:
        # result in chars that do not have the affect of ' in sql terms
        text = text.replace("\"","&quot;")
        text = text.replace("'","&#x27")
        return text
    @staticmethod
    def edit_request(request: Request) -> Request:
        request.url = SQLI_Preventer.replace_sql(request.url)
        new_headers = {}
        for key,val in request.headers.items():
            new_headers[key] = SQLI_Preventer.replace_sql(val)
        request.headers = new_headers
        if isinstance(request.data, str):#if data isn't str, we do not need to check it
            request.data = SQLI_Preventer.replace_sql(request.data)
        return request
