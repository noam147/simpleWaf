import socket
import unlogged_user_menu
#import logged_user_menu
def handle_user(sock):
    current_state = unlogged_user_menu.Unlogged_user()
    while True:
        current_state = current_state.handle_user(sock)
        if current_state == None:
            current_state = unlogged_user_menu.Unlogged_user()