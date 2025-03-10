from client_program import check_status_after_exec, get_menu, UNLOGGED_SCREEN, EXIT
import json
import socket_client

available_commands = ['See Preferences','Set Preferences','Change Details Of User','Log Out','Delete User', 'Delete Web From WAF Defence System', 'Exit']

dict_available_commands = {index: command for index, command in enumerate(available_commands,1)}
SEE_PREFERENCES_CODE = chr(5)
SET_PREFERENCES_CODE = chr(6)
CHANGE_DETAILS_OF_USER_CODE = chr(7)
SEE_LOG_FILE_CODE = chr(8)
LOGOUT_CODE = chr(9)
#todo add msg codes of delete user and web and their funs
def see_preferences():
    """because the server save at its side the username we won't need send anything but the msgcode"""
    full_msg = SEE_PREFERENCES_CODE + "{}"
    socket_client.send_data(full_msg)
    answer = socket_client.receive_data()
    #todo prase the answer for better looking
    msg_from_server = json.loads(answer)
    print(answer)


@check_status_after_exec
def set_preferences():
    """func will ask user to fill all inputs, the validation will happen at server side"""
    sql_level = input("enter sqlLevel[int from 0-2]: ")
    xss_defence = input('XSS defence: [Y/y] for Yes other for no')
    xss_defence = True if xss_defence.lower() == 'y' else False
    hpp_defence = input('HPP defence: [Y/y] for Yes other for no')
    hpp_defence = True if hpp_defence.lower() == 'y' else False
    file_attack_level = input("File Attacks Level[int from 0-2]: ")
    to_send_email =input('Send email when attacked?: [Y/y] for Yes other for no')
    to_send_email = True if to_send_email.lower() == 'y' else False
    os_level = input("OS:\nEnter 0 for Linux defence.\nEnter 1 for Windows defence.\nEnter something else for no defence of OS.")
    port = input('enter port for routing:\n')
    isHttps = input('using HTTPS?: [Y/y] for Yes other for HTTP')
    isHttps = True if isHttps.lower() == 'y' else False
    final_dict = {
            "sql_level": sql_level,
            "xss_defence": xss_defence,
            "hpp_defence": hpp_defence,
            "file_attack_level": file_attack_level,
            "to_send_email": to_send_email,
            "os_level": os_level,
            "port": port,
            "isHttps": isHttps
        }

    full_msg = SET_PREFERENCES_CODE + json.dumps(final_dict)
    socket_client.send_data(full_msg)
def logged_user():
    menu = get_menu(available_commands)
    while True:
        print(menu)
        current_choice = int(input())
        actual_command = dict_available_commands[current_choice]
        print(actual_command)
        if actual_command == 'See Preferences':
            see_preferences()
        elif actual_command == 'Set Preferences':
            set_preferences()
        elif actual_command == 'Log Out':
            full_msg = LOGOUT_CODE + ""
            socket_client.send_data(full_msg)
            return UNLOGGED_SCREEN
        elif actual_command == 'Exit':
            return EXIT
        else:
            print('Try Again.')