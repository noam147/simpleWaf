
from Attack_Preventer import Attack_Scanner
from requests import Request
class XSS_Preventer(Attack_Scanner):
    @staticmethod
    def replace_xss(text:str) -> str:
        # result in chars that do not have the affect of > in xss terms
        text = text.replace("<","&lt")
        text = text.replace(">","&gt")
        return text
    @staticmethod
    def edit_request(request: Request) -> Request:
        request.url = XSS_Preventer.replace_xss(request.url)
        new_headers = {}
        for key,val in request.headers.items():
            new_headers[key] = XSS_Preventer.replace_xss(val)
        request.headers = new_headers
        if isinstance(request.data, str):#if data isn't str, we do not need to check it
            request.data = XSS_Preventer.replace_xss(request.data)
        return request
