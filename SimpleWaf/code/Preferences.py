"""the method for reducing running time is to save the websites pref in a dict
and then just extrqact the data
the dict will be updated in 24h(each new day)"""
import DB_Wrapper
from Preferences_Items import  Preferences_Items
SQL_LEVEL = "sqli_defence_level"
FILES_LEVEL = "file_attacks_level"
XSS_LEVEL = "xss_defence"
hpp_defence = "a"

### send an email to the website owner ###
SEND_EMAIL = "send_email_when_attacked"

### 0: linux, 1: windows, 2: other(does not get check)
OS = "osLevel"

### ddos and slow loris are excluded because they are also harming the WAF itself and not the just the websites ###


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

##update the table prefrnces ###
DB_Wrapper.drop_table("Preferences")
# create again
DB_Wrapper.create_tables()

example_of_settings_updations = [("facebook.com",3,True,True,3,True,1)]
pref_items = Preferences_Items(example_of_settings_updations)
DB_Wrapper.special_insert_or_update_preferences_table_pref_items(pref_items)
## call to update the dict (in prodaction this will be called once in 24H)
Preferences.update_dict()

print(Preferences.get_preferences_of_website("facebook.com").to_string())