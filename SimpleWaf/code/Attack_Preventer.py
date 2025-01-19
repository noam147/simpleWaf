
"""
this is an interface for attacks that can be prevented via change some parts from the msg, without harming the content
for each attack the web will decide if he wants to prevent it or keep it as is
"""
from tornado.httputil import HTTPServerRequest
from abc import ABC, abstractmethod
#abc- Abstract Base Classes
class Attack_Scanner(ABC):
    @staticmethod
    @abstractmethod
    def edit_request(request: HTTPServerRequest) -> HTTPServerRequest:
        """
        searches the attack in the data, will return True if attack found(False if not)
        assumption: the data is already decoded
        this is a real solution that many webs are using.
        """
        pass