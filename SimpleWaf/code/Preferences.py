"""the method for reducing running time is to save the websites pref in a dict
and then just extrqact the data
the dict will be updated in 24h(each new day)"""
import DB_Wrapper
from Preferences_Items import Preferences_Items
import time
import threading
### ddos and slow loris are excluded because they are also harming the WAF itself and not just the websites ###

class Preferences:
    preferences_dict = {}

    @staticmethod
    def __sleep_and_update():
        while True:
            Preferences.update_dict()
            # 24 hours...
            time.sleep(60 * 60 * 24)
    @staticmethod
    def at_start():
        t = threading.Thread(target=Preferences.__sleep_and_update)
        t.daemon = True
        t.start()
        #make detach of thread each 24 hours - execc update dict
    @staticmethod
    def update_dict():
        """this func will update the dict - insert new registered websites and update their defence level"""
        host_names = DB_Wrapper.get_all_host_names()
        for host in host_names:
            actual_host_name:str = host[0]
            actual_host_name = actual_host_name.lower()
            curr_pref = DB_Wrapper.get_preferences_by_host_name(actual_host_name)
            Preferences.preferences_dict[actual_host_name] = curr_pref
    @staticmethod
    def get_generic_prefs(host_name:str) -> Preferences_Items:
        return Preferences_Items([(host_name,2,True,True,2,False,2,443,True)])
    @staticmethod
    def get_preferences_of_website(host_name:str) -> Preferences_Items:
        """func will return a Preferences_Items that contains the website preferences for attacks"""
        """if the website is not in the dict, return null"""
        try:
            host_name = host_name.lower()
            return Preferences.preferences_dict[host_name]
        except Exception as e:
            print(e)
            return None#if web not in db

