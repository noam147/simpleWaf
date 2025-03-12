import socket
import unlogged_user_menu
def handle_user(sock):
    #cuurent state can be logged or unlogged
    current_state = unlogged_user_menu.Unlogged_user()
    while True:
        current_state = current_state.handle_user(sock)
        if current_state == None:
            current_state = unlogged_user_menu.Unlogged_user()