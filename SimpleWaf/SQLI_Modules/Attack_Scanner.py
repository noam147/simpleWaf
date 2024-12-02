"""
this is an interface for attack scanners
"""
class IAttack_Scanner:
    @staticmethod
    def scan(data: str) -> bool:
        """
        searches the attack in the data, will return True if attack found(False if not)
        """
        pass