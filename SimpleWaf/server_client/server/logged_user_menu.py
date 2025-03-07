import socket
from General_Handler_Class import GeneralHandler
from unlogged_user_menu import Unlogged_user
import json
from things_for_all_handlers import receive_data,send_data
"""how to know to which web are we using? maybe pass the user name.."""
SEE_PREFERENCES_CODE = chr(5)
SET_PREFERENCES_CODE = chr(6)
CHANGE_DETAILS_OF_USER_CODE = chr(7)
SEE_LOG_FILE_CODE = chr(8)
LOGOUT_CODE = chr(9)
available_commands = ['See Preferences','Set Preferences','Change Details Of User','Print Menu','Log Out','Exit']

def see_preferences(json_msg):
    print("see_preferences")
    pass
def set_preferences(json_msg):
    pass
def change_details_of_user(json_msg):
    pass
def see_log_file(json_msg):
    pass
class Logged_user(GeneralHandler):
    def handle_user(self,client_socket: socket.socket):
        msg = receive_data(client_socket)
        code_msg = msg[0]
        try:
            json_msg = json.loads(msg[1:])
        except Exception as e:
            send_data(client_socket, "Invalid request.")
            return self
        if code_msg == SEE_PREFERENCES_CODE:
            result = see_preferences(json_msg)
        elif code_msg == SET_PREFERENCES_CODE:
            result = set_preferences(json_msg)
        elif code_msg == CHANGE_DETAILS_OF_USER_CODE:
            result = change_details_of_user(json_msg)
        elif code_msg == SEE_LOG_FILE_CODE:
            result = see_log_file(json_msg)
        elif code_msg == LOGOUT_CODE:
            data = {'isSuccesses': True, 'explanation': ''}
            send_data(client_socket, json.dumps(data))
            return Unlogged_user()
            ###if result is true, we pass user into the second handler like trivia###
        else:
            data = {'isSuccesses': False, 'explanation': '---Invalid Code Msg---'}
            send_data(client_socket, json.dumps(data))
            return self
        data = {'isSuccesses': result[0], 'explanation': result[1]}
        send_data(client_socket, json.dumps(data))
        return self