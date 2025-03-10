import socket
from General_Handler_Class import GeneralHandler
#from unlogged_user_menu import Unlogged_user
import json
from things_for_all_handlers import receive_data,send_data
import DB_Wrapper
from Preferences_Items import Preferences_Items
"""how to know to which web are we using? maybe pass the user name.."""
SEE_PREFERENCES_CODE = chr(5)
SET_PREFERENCES_CODE = chr(6)
CHANGE_DETAILS_OF_USER_CODE = chr(7)
SEE_LOG_FILE_CODE = chr(8)
LOGOUT_CODE = chr(9)
available_commands = ['See Preferences','Set Preferences','Change Details Of User','Print Menu','Log Out','Exit']

def see_preferences(host_name:str) -> tuple[bool,dict]:
    print("see_preferences")
    result: Preferences_Items = DB_Wrapper.get_preferences_by_host_name(host_name)
    result_in_dict = result.to_dict()
    return True, result_in_dict
def set_preferences(json_msg, host_name):
    print(host_name)
    print(json_msg)
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
    pass
def see_log_file(json_msg):
    pass
class Logged_user(GeneralHandler):
    def __init__(self,username):
        self.username:str = username
        self.hostname:str = DB_Wrapper.get_host_name_for_user(username)
        if self.hostname == None or self.hostname == "":
            print("hostname is None or empty. should not happend. abort.")
            raise Exception
        #get the host name by username or do that for each host_name there will be separate users to allow multiple user names for difrrent hostnames
        #self.host_name = host_name
    def handle_user(self,client_socket: socket.socket):
        print("username is: ")
        print(self.username)
        msg = receive_data(client_socket)
        code_msg = msg[0]
        try:
            json_msg = json.loads(msg[1:])
        except Exception as e:
            send_data(client_socket, "Invalid request.")
            return self
        if code_msg == SEE_PREFERENCES_CODE:
            result = see_preferences(self.hostname)
        elif code_msg == SET_PREFERENCES_CODE:
            result = set_preferences(json_msg,self.hostname)
        elif code_msg == CHANGE_DETAILS_OF_USER_CODE:
            result = change_details_of_user(json_msg)
        elif code_msg == SEE_LOG_FILE_CODE:
            result = see_log_file(json_msg)
        elif code_msg == LOGOUT_CODE:
            data = {'isSuccesses': True, 'explanation': ''}
            send_data(client_socket, json.dumps(data))
            return None
            ###if result is true, we pass user into the second handler like trivia###
        else:
            data = {'isSuccesses': False, 'explanation': '---Invalid Code Msg---'}
            send_data(client_socket, json.dumps(data))
            return self
        data = {'isSuccesses': result[0], 'explanation': result[1]}
        send_data(client_socket, json.dumps(data))
        return self