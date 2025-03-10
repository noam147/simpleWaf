import guiStaff
import json
import socket_client
LOGGED_SCREEN = "logged_user_screen"
UNLOGGED_SCREEN = "unlogged_user_screen"
EXIT = "exit"
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


def get_menu(available_commands:list) -> str:
    """func for having nice menu"""
    menu = "Available Commands:\n"
    for i in range(len(available_commands)):
        menu += f"[{i+1}]. {available_commands[i]}\n"
    return menu[:-1]#without the last \n


def at_start():
    from unlogged_client import unlogged_user
    from logged_client import logged_user
    if not socket_client.at_start():
        print("Server is not Available Right Now.")
        return -1
    print(guiStaff.start_of_screen)
    result = unlogged_user()
    while True:
        if result == EXIT:
            return 1
        elif result == LOGGED_SCREEN:
            result = logged_user()#assign new result code
        elif result == UNLOGGED_SCREEN:
            result = unlogged_user()
        else:
            return -1





if __name__ == '__main__':
    at_start()