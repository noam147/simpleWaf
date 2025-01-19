"""the method for reducing running time is to save the websites pref in a dict
and then just extrqact the data
the dict will be updated in 24h(each new day)"""
import DB_Wrapper
from Preferences_Items import  Preferences_Items
### ddos and slow loris are excluded because they are also harming the WAF itself and not just the websites ###

class Preferences:
    preferences_dict = {}
    @staticmethod
    def at_start():
        pass#make detach of thread each 24 hours - execc update dict
    @staticmethod
    def update_dict():
        """this func will update the dict - insert new registered websites and update their defence level"""
        host_names = DB_Wrapper.get_all_host_names()
        for host in host_names:
            actual_host_name = host[0]
            curr_pref = DB_Wrapper.get_preferences_by_host_name(actual_host_name)
            curr_pref_in_class = Preferences_Items(curr_pref)
            Preferences.preferences_dict[actual_host_name] = curr_pref_in_class
        pass
    @staticmethod
    def get_preferences_of_website(host_name:str) -> Preferences_Items:
        """func will return a Preferences_Items that contains the website preferences for attacks"""
        """if the website is not in the dict, return null"""
        try:
            return Preferences.preferences_dict[host_name]
        except Exception:
            return None#if web not in db

