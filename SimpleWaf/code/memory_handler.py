from datetime import datetime

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
            del data_dict[ATTACKERS][ip_add]
            return False
        return True
    except KeyError:
        #Key not found in dictionary#
        return False
    except Exception as e:
        print(e)
        return False
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
    # those will be kept as
    #data_dict[ATTACKERS] = DB_Wrapper.get_table_values(ATTACKERS)
    #data_dict[ATTACKERS_SCORE] = DB_Wrapper.get_table_values(ATTACKERS_SCORE)
    print(data_dict)

if __name__ == '__main__':
    example_of_getting_data()