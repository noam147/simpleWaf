
from Attack_Preventer import Attack_Scanner
from tornado.httputil import HTTPServerRequest
from copy import deepcopy
class XSS_Preventer(Attack_Scanner):
    @staticmethod
    def replace_xss(text:str) -> str:
        # result in chars that do not have the affect of > in xss terms
        text = text.replace("<","&lt;")
        text = text.replace(">","&gt;")
        return text
    @staticmethod
    def edit_request(request: HTTPServerRequest) -> HTTPServerRequest:
        request.uri = XSS_Preventer.replace_xss(request.uri)
        new_headers = {}
        for key,val in request.headers.items():
            new_headers[key] = XSS_Preventer.replace_xss(val)
        request.headers = new_headers
        #if request.body and isinstance(request.body, str):#if data isn't str, we do not need to check it
        #    request.data = XSS_Preventer.replace_xss(request.body)
        if request.body:
            request.body = XSS_Preventer.replace_xss(request.body.decode() if isinstance(request.body,bytes) else request.body)
        return request
