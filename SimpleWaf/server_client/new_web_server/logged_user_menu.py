import DB_Wrapper
from Preferences_Items import Preferences_Items
import waf_handler

def see_preferences(host_name:str) -> tuple[bool,dict]:
    result: Preferences_Items = DB_Wrapper.get_preferences_by_host_name(host_name)
    result_in_dict = result.to_dict()
    return True, result_in_dict
def set_preferences(json_msg, host_name) -> tuple[bool,str]:
    pref_from_json = []
    try:
        pref_from_json.append(host_name)
        pref_from_json.append(json_msg["sql_level"])
        pref_from_json.append(json_msg["xss_defence"])
        pref_from_json.append(json_msg["hpp_defence"])
        pref_from_json.append(json_msg["file_attack_level"])
        pref_from_json.append(json_msg["to_send_email"])
        pref_from_json.append(json_msg["os_level"])
        pref_from_json.append(json_msg["port"])
        pref_from_json.append(json_msg["isHttps"])
    except Exception as e:
        return False, "msg is corrupted, check json values"
    from waf_handler import update_prefs
    print("update prefs")
    update_prefs(json_msg,host_name)
    DB_Wrapper.special_insert_or_update_preferences_table_preferences_table(Preferences_Items([pref_from_json]))
    return True, ""
def change_details_of_user(json_msg):
    #can change the password, the email add, and maybe its username?
    #should we allow also the host name to be changed?
    pass
def see_log_file(host_name:str):
    return True, waf_handler.get_log_file_of_web(host_name)
