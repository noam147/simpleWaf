from abc import ABC, abstractmethod
import socket
class GeneralHandler(ABC):  #just like trivia
    @abstractmethod
    def handle_user(self,client_socket: socket.socket) -> "GeneralHandler": #because the class is not definded yet we put this in ""
        pass
