import guiStaff
import json
import socket_client
available_commands = ['Help','Add Website','Add User','Print Menu','Log In','Exit']

dict_available_commands = {index: command for index, command in enumerate(available_commands,1)}
ADD_USER_MSG_CODE = chr(1)
ADD_WEBSITE_MSG_CODE = chr(2)
LOGIN_CODE = chr(3)
def check_status_after_exec(func):
    """this func is a decorator for reducing lines of duplicate code"""
    def wrapper(*args, **kwargs):
        func(*args, **kwargs)
        status = socket_client.receive_data()
        msg_from_server = json.loads(status)
        if msg_from_server['isSuccesses']:
            print('Operation Successes.')
        else:
            print(msg_from_server['explanation'])
        return msg_from_server['isSuccesses']#return this for when we need to see if operation was good
    return wrapper


def get_menu():
    menu = "Available Commands:\n"
    for i in range(len(available_commands)):
        menu += f"[{i+1}]. {available_commands[i]}\n"
    return menu[:-1]#without the last \n

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
    #todo if the server return okey we will direct the user into phase 2
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
def main_from_server():
    if not socket_client.at_start():
        print("Server is not Available Right Now.")
        return -1
    while True:
        msg_from_server = socket_client.receive_data()
        print(msg_from_server)
        msg_from_client = input()
        socket_client.send_data(msg_from_client)
def main():
    if not socket_client.at_start():
        print("Server is not Available Right Now.")
        return -1
    menu = get_menu()
    print(guiStaff.start_of_screen)
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
                pass#todo show the user commands of logged user
        elif actual_command == 'Exit':
            break
        else:
            print('Try Again.')


if __name__ == '__main__':
    main()