import socket
import json
from things_for_all_handlers import receive_data,send_data
available_commands = ['Help','Add Website','Add User','Print Menu','Log In','Exit']

dict_available_commands = {index: command for index, command in enumerate(available_commands,1)}


ADD_USER_MSG_CODE = chr(1)
ADD_WEBSITE_MSG_CODE = chr(2)

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
    except Exception:
        return False,"msg is corrupted, check json values"

    return True,""
def add_website(json_msg) -> tuple[bool,str]:
    try:
        host_name = json_msg["host_name"]
        ip_add = json_msg["ip_add"]
    except Exception:
        return False, "msg is corrupted, check json values"

    return True,""


#### way of operation - user will send a msmg code and after that details in json like trivia.......

def handel_user(client_socket:socket.socket,client_address):
    while True:
        result = False
        msg = receive_data(client_socket)
        code_msg = msg[0]
        try:
            json_msg = json.loads(msg[1:])
        except Exception as e:
            send_data(client_socket,"Invalid request.")
            continue
        func_to_activate = None
        if code_msg == ADD_USER_MSG_CODE:
            func_to_activate = add_user
        elif code_msg == ADD_WEBSITE_MSG_CODE:
            func_to_activate = add_website

        if func_to_activate == None:
            data = {'isSuccesses':False,'explanation': '---Invalid Code Msg---'}
            send_data(client_socket, json.dumps(data))
            continue
        result = func_to_activate(json_msg)
        data = {'isSuccesses':result[0],'explanation':result[1]}
        send_data(client_socket,json.dumps(data))

    while True:
        current_choice = receive_data(client_socket)
        try:
            current_choice = int(current_choice)
        except Exception:
            continue
        actual_command = dict_available_commands[current_choice]
        print(actual_command)
        if actual_command == 'Add User':
            add_user(client_socket)
        elif actual_command == 'Add Website':
            add_website(client_socket)
        elif actual_command == 'Exit':
            break
        else:
            send_data(client_socket,'Try Again.')