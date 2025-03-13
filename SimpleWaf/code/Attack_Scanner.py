"""
this is an interface for attack scanners
"""
import requests
from abc import ABC, abstractmethod
#abc- Abstract Base Classes
class IAttack_Scanner(ABC):
    @staticmethod
    @abstractmethod
    def scan(data: requests.Request,pref_of_web) -> bool:
        """
        searches the attack in the data, will return True if attack found(False if not)
        assumption: the data is already decoded
        pref_of_web is dynamically typed based on each attack pref(can be bool or int for now)
        """
        pass