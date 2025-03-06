import socket
import json
from things_for_all_handlers import receive_data,send_data
import DB_Wrapper
available_commands = ['Help','Add Website','Add User','Print Menu','Log In','Exit']

dict_available_commands = {index: command for index, command in enumerate(available_commands,1)}


ADD_USER_MSG_CODE = chr(1)
ADD_WEBSITE_MSG_CODE = chr(2)
LOGIN_CODE = chr(3)
#generic func for all handlers:
def get_menu():
    menu = "Available Commands:\n"
    for i in range(len(available_commands)):
        menu += f"[{i+1}]. {available_commands[i]}\n"
    return menu[:-1]#without the last \n

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
        host_name = json_msg["host_name"]
        ip_add = json_msg["ip_add"]
    except Exception:
        return False, "msg is corrupted, check json values"
    DB_Wrapper.special_insert_or_update_website_ip(host_name, ip_add)
    return True,""
def login(json_msg) -> tuple[bool,str]:
    try:
        username = json_msg["username"]
        password = json_msg["password"]
    except Exception:
        return False,"msg is corrupted, check json values"
    if DB_Wrapper.verify_login_into_website_login(username, password):
        return True,""
    return False,"login failed"

#### way of operation - user will send a msmg code and after that details in json like trivia.......

def handel_user(client_socket:socket.socket,client_address):
    DB_Wrapper.print_table_values('website_login')
    DB_Wrapper.print_table_values('websites_ip')
    while True:
        result = False
        msg = receive_data(client_socket)
        code_msg = msg[0]
        try:
            json_msg = json.loads(msg[1:])
        except Exception as e:
            send_data(client_socket,"Invalid request.")
            continue
        if code_msg == ADD_USER_MSG_CODE:
            result = add_user(json_msg)
        elif code_msg == ADD_WEBSITE_MSG_CODE:
            result = add_website(json_msg)
        elif code_msg == LOGIN_CODE:
            result = login(json_msg)
            if result[0]:#if login good
                pass#todo pass user to second phase
            ###if result is true, we pass user into the second handler like trivia###
        else:
            data = {'isSuccesses':False,'explanation': '---Invalid Code Msg---'}
            send_data(client_socket, json.dumps(data))
            continue
        data = {'isSuccesses':result[0],'explanation':result[1]}
        send_data(client_socket, json.dumps(data))