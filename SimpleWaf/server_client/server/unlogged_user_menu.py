import socket
import json
from General_Handler_Class import GeneralHandler
from logged_user_menu import Logged_user
from things_for_all_handlers import receive_data,send_data
import DB_Wrapper

ADD_USER_MSG_CODE = chr(1)
ADD_WEBSITE_MSG_CODE = chr(2)
LOGIN_CODE = chr(3)

def add_user(json_msg) -> tuple[bool,str]:
    ### bool is result if went good, str is an explnation of what happend wrong###
    try:
        host_name = json_msg["host_name"]
        username = json_msg["username"]
        password = json_msg["password"]
        email = json_msg["email"]
    except Exception:
        return False,"msg is corrupted, check json values"
    if not DB_Wrapper.get_if_host_name_exist(host_name):
        return False,"Error with host_name, sign up your website before."
    if DB_Wrapper.check_if_username_exist_in_website_login(username):
        return False, "username already existing."
    if DB_Wrapper.insert_into_website_login(host_name,username,password,email):
        return True,""
    return False,"error with db"
def add_website(json_msg) -> tuple[bool,str]:
    try:
        host_name:str = json_msg["host_name"]
        ip_add = json_msg["ip_add"]
    except Exception:
        return False, "msg is corrupted, check json values"
    host_name = host_name.lower()#to prevent mismtach in capitals.
    DB_Wrapper.special_insert_or_update_website_ip(host_name, ip_add)
    return True,""
def login(json_msg) -> tuple[bool,str]:
    try:
        username = json_msg["username"]
        password = json_msg["password"]
    except Exception:
        return False,"msg is corrupted, check json values"
    if DB_Wrapper.verify_login_into_website_login(username, password):
        return True,username
    return False,"login failed"

#### way of operation - user will send a msmg code and after that details in json like trivia.......
class Unlogged_user(GeneralHandler):
    def handle_user(self,client_socket: socket.socket):
        msg = receive_data(client_socket)
        code_msg = msg[0]
        try:
            #just like trivia
            json_msg = json.loads(msg[1:])
        except Exception as e:
            send_data(client_socket, "Invalid request.")
            return self
        if code_msg == ADD_USER_MSG_CODE:
            result = add_user(json_msg)
        elif code_msg == ADD_WEBSITE_MSG_CODE:
            result = add_website(json_msg)
        elif code_msg == LOGIN_CODE:
            result = login(json_msg)
            if result[0]:  # if login good
                data = {'isSuccesses': True, 'explanation': ''}
                send_data(client_socket, json.dumps(data))
                username = result[1]
                return Logged_user(username) #pass user to second phase
            ###if result is true, we pass user into the second handler like trivia###
        else:
            data = {'isSuccesses': False, 'explanation': '---Invalid Code Msg---'}
            send_data(client_socket, json.dumps(data))
            return self
        data = {'isSuccesses': result[0], 'explanation': result[1]}
        send_data(client_socket, json.dumps(data))
        return self