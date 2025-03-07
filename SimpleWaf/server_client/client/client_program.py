import guiStaff
import json
import socket_client
from unlogged_client import unlogged_user

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


def get_menu(available_commands:list):
    menu = "Available Commands:\n"
    for i in range(len(available_commands)):
        menu += f"[{i+1}]. {available_commands[i]}\n"
    return menu[:-1]#without the last \n


def at_start():
    if not socket_client.at_start():
        print("Server is not Available Right Now.")
        return -1
    print(guiStaff.start_of_screen)
    unlogged_user()



if __name__ == '__main__':
    at_start()