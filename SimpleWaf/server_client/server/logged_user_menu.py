import socket
from General_Handler_Class import GeneralHandler
import json
from things_for_all_handlers import receive_data, send_data
import DB_Wrapper
from Preferences_Items import Preferences_Items
import waf_handler
SEE_PREFERENCES_CODE = chr(5)
SET_PREFERENCES_CODE = chr(6)
CHANGE_DETAILS_OF_USER_CODE = chr(7)
SEE_LOG_FILE_CODE = chr(8)
LOGOUT_CODE = chr(9)
available_commands = ['See Preferences','Set Preferences','Change Details Of User','Print Menu','Log Out','Exit']

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
    DB_Wrapper.special_insert_or_update_preferences_table_preferences_table(Preferences_Items([pref_from_json]))
    return True, ""
def change_details_of_user(json_msg):
    #can change the password, the email add, and maybe its username?
    #should we allow also the host name to be changed?
    pass
def see_log_file(host_name:str):
    return True, waf_handler.get_log_file_of_web(host_name)
class Logged_user(GeneralHandler):
    def __init__(self,username):
        self.username:str = username
        #because the username is unique we can be sure it matches only one corresponding hostname
        self.hostname:str = DB_Wrapper.get_host_name_for_user(username)
        if self.hostname == None or self.hostname == "":
            print("hostname is None or empty. should not happend. abort.")
            raise Exception
    def handle_user(self,client_socket: socket.socket,current_msg:str):
        code_msg = current_msg[0]
        try:
            json_msg = json.loads(current_msg[1:])
        except Exception as e:
            send_data(client_socket, "Invalid request.")
            return self
        if code_msg == SEE_PREFERENCES_CODE:
            result = see_preferences(self.hostname)
        elif code_msg == SET_PREFERENCES_CODE:
            result = set_preferences(json_msg, self.hostname)
        elif code_msg == CHANGE_DETAILS_OF_USER_CODE:
            result = change_details_of_user(json_msg)
        elif code_msg == SEE_LOG_FILE_CODE:
            result = see_log_file(self.hostname)
        elif code_msg == LOGOUT_CODE:
            #we will not send data back to the user, there is no need to.
            data = {'isSuccesses': True, 'explanation': ''}
            send_data(client_socket, json.dumps(data))
            return None#none means to get back into unlogged

        else:
            #if msg of user did not match known msgcode
            data = {'isSuccesses': False, 'explanation': '---Invalid Code Msg---'}
            send_data(client_socket, json.dumps(data))
            return self
        data = {'isSuccesses': result[0], 'explanation': result[1]}
        send_data(client_socket, json.dumps(data))
        return self