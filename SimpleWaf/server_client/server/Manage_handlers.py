import socket
import unlogged_user_menu
import waf_handler
def handle_user(sock:socket.socket):
    msg = sock.recv(2056).decode('utf-8')
    if waf_handler.check_if_msg_from_waf(msg):
        waf_handler.handle_waf(sock, msg)
        return
    #cuurent state can be logged or unlogged
    current_state = unlogged_user_menu.Unlogged_user()
    while True:
        current_state = current_state.handle_user(sock, msg)
        if current_state == None:
            current_state = unlogged_user_menu.Unlogged_user()
        msg = sock.recv(2056).decode('utf-8')