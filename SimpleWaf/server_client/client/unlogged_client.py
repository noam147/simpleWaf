from client_program import check_status_after_exec, get_menu, LOGGED_SCREEN, EXIT
import json
import socket_client

available_commands = ['Add Website','Add User','Print Menu','Log In','Exit']

dict_available_commands = {index: command for index, command in enumerate(available_commands,1)}
ADD_USER_MSG_CODE = chr(1)
ADD_WEBSITE_MSG_CODE = chr(2)
LOGIN_CODE = chr(3)

@check_status_after_exec
def add_user():
    print('---Add User Selected---')
    host_name = input("Enter Host Name of Website That Signed To WAF:\n")
    username = input("Enter User Name:\n")
    password = input('Enter Password For User:\n')
    email = input("Enter email for User:(can be change later)\n")
    data = {
        'host_name': host_name,
        'username':username,
        'password': password,
        'email':email

    }
    json_str = json.dumps(data)

    full_msg = ADD_USER_MSG_CODE + json_str
    socket_client.send_data(full_msg)
    #print('---User Added Successfully---')
@check_status_after_exec
def log_in():
    print('---login Selected---')
    username = input("Enter User Name:\n")
    password = input('Enter Password For User:\n')
    data = {
        'username': username,
        'password': password,
    }
    json_str = json.dumps(data)
    full_msg = LOGIN_CODE + json_str
    socket_client.send_data(full_msg)
    #if the server return okey we will direct the user into phase 2
@check_status_after_exec
def add_website():
    print('---Add Website Selected---')
    host_name = input("Enter Host Name of Website to Sign to WAF:\n")
    ip_add = input("Enter IP Address:\n")

    data = {
        'host_name': host_name,
        'ip_add':ip_add
    }
    json_str = json.dumps(data)

    full_msg = ADD_WEBSITE_MSG_CODE + json_str
    socket_client.send_data(full_msg)
    #print('---Website Added Successfully---')
def unlogged_user():
    menu = get_menu(available_commands)
    while True:
        print(menu)
        current_choice = int(input())
        actual_command = dict_available_commands[current_choice]
        print(actual_command)
        if actual_command == 'Add User':
            add_user()
        elif actual_command == 'Add Website':
            add_website()
        elif actual_command == 'Log In':
            result = log_in()
            if result:
                print("Logged In. Passing to New menu.")#todo show the user commands of logged user
                return LOGGED_SCREEN
        elif actual_command == 'Exit':
            return EXIT
        else:
            print('Try Again.')