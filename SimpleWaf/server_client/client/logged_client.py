from client_program import check_status_after_exec, get_menu
import json
import socket_client

available_commands = ['See Preferences','Set Preferences','Change Details Of User','Print Menu','Log Out','Exit']

dict_available_commands = {index: command for index, command in enumerate(available_commands,1)}
SEE_PREFERENCES_CODE = chr(5)
SET_PREFERENCES_CODE = chr(6)
CHANGE_DETAILS_OF_USER_CODE = chr(7)
SEE_LOG_FILE_CODE = chr(8)
LOGOUT_CODE = chr(9)

def logged_user(username:str):
    menu = get_menu(available_commands)
    while True:
        print(menu)
        current_choice = int(input())
        actual_command = dict_available_commands[current_choice]
        print(actual_command)
        if actual_command == 'See Preferences':
            pass
        elif actual_command == 'Set Preferences':
            pass
        elif actual_command == 'Log Out':
            full_msg = LOGOUT_CODE + ""
            socket_client.send_data(full_msg)
            return
        elif actual_command == 'Exit':
            break
        else:
            print('Try Again.')