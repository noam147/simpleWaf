from datetime import datetime

import Preferences

### this file will contain the data that the waf will use ###
### this is baisicly the db data - but in memory for better performance ###

# first we want to create the initial dict #
data_dict = {}
attackers_dict = {}
# second we want to have our values&keys #
# each value is name of db table and the key is empty dict - each row in db is value and the host name is key when possible
#tables: websites_ip, website_login, attackers, attackers_score, preferences

# we will assign each table name to a global const var, this will function as a define if for some reason we want to replace the name#
WEBSITES_IP = 'websites_ip'
WEBSITE_LOGIN = 'website_login'
ATTACKERS = 'attackers'
ATTACKERS_SCORE = 'attackers_score'
PREFERENCES = 'preferences'


def init_dict() -> None:
    #assgin:
    data_dict[WEBSITES_IP] = []
    data_dict[WEBSITE_LOGIN] = []
    data_dict[ATTACKERS] = []
    data_dict[ATTACKERS_SCORE] = []
    data_dict[PREFERENCES] = []
def get_ip_by_host_name(host_name:str):
    host_name = host_name.lower()
    ### func will return the ip as string or None if there isn't
    try:
        return data_dict[WEBSITES_IP][host_name]
    except Exception:
        return None
def get_is_ip_attacker(ip_add:str) -> bool:
    try:
        #str at start:
        attacker_free_date = data_dict[ATTACKERS][ip_add]
        #convert the attacker free date from str:
        attacker_free_date = datetime.strptime(attacker_free_date, '%Y-%m-%d')

        current_date = datetime.now()
        # if the attacker_free_date already past
        if current_date > attacker_free_date:
            #todo maybe alert the server? or the server will do checking of his own?
            del data_dict[ATTACKERS][ip_add]
            return False
        return True
    except KeyError:
        #Key not found in dictionary#
        return False
    except Exception as e:
        print(e)
        return False
def get_prefs_of_web(hostname:str) -> Preferences.Preferences_Items:
    try:
        hostname = hostname.lower()
        prefs = data_dict[PREFERENCES][hostname]
        return Preferences.Preferences_Items([prefs])
    except Exception:
        return None
def get_data_from_server(websites_ip_table_vals,preferences_table_vals,attackers_table_vals):
    data_dict[WEBSITES_IP] = {}
    for curr_web in websites_ip_table_vals:
        host_name: str = curr_web[0]
        host_name = host_name.lower()
        ip_add: str = curr_web[1]
        data_dict[WEBSITES_IP][host_name] = ip_add

def example_of_getting_data():
    ### in the real case, we will get the info from the other server when the WAF starts ###
    ##
    import DB_Wrapper
    data_dict[WEBSITES_IP] = {}
    webs_info = DB_Wrapper.get_table_values(WEBSITES_IP)
    for curr_web in webs_info:
        host_name:str = curr_web[0]
        host_name = host_name.lower()
        ip_add:str = curr_web[1]
        data_dict[WEBSITES_IP][host_name] = ip_add
    ### the waf does not need the login creds ###
    #data_dict[WEBSITE_LOGIN] = DB_Wrapper.get_table_values(WEBSITE_LOGIN)

    data_dict[PREFERENCES] = {}
    prefs = DB_Wrapper.get_table_values(PREFERENCES)
    for curr_pref in prefs:
        host_name:str = curr_pref[0]
        host_name = host_name.lower()
        # for better lookup time in runtime #
        data_dict[PREFERENCES][host_name] = curr_pref

    ### the attackers dict will contain the key ip and value free date
    data_dict[ATTACKERS] = {}
    # those will be kept as normal dict
    attackers_data = DB_Wrapper.get_table_values(ATTACKERS)
    for data_cell in attackers_data:
        attacker_ip = data_cell[0]
        attacker_freedate = data_cell[1]
        str_attacker_free_date = attacker_freedate.strftime("%Y-%m-%d")
        data_dict[ATTACKERS][attacker_ip] = str_attacker_free_date

    ### attackers score is not relevant to the WAF - that is just the server handling ###
    # todo think about when the waf will get updated from the server
    #       data_dict[ATTACKERS_SCORE] = DB_Wrapper.get_table_values(ATTACKERS_SCORE)
    print(data_dict[ATTACKERS])

if __name__ == '__main__':
    example_of_getting_data()
    ### activate this on attacker ip with date that did not pass ###
    print(get_is_ip_attacker('123.123.123.123'))
