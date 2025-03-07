import socket
import threading
from Manage_handlers import handle_user
IP_ADD = '0.0.0.0'
SERVER_PORT = 47777
server_socket:socket.socket = None



def at_start() -> bool:
    """return true if the server established"""
    global server_socket
    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((IP_ADD, SERVER_PORT))
        server_socket.listen()
    except Exception as e:
        return False
    return True
def accept_client():
    print("Server now accepting clients.")
    global server_socket
    while True:
        client_socket, client_address = server_socket.accept()
        print(client_socket)
        print(client_address)
        #todo pass them in thread to treat them
        #client_socket.send(guiStaff.start_of_screen)
        t = threading.Thread(target=handle_user,args =(client_socket,))
        t.daemon = True
        t.start()
        #handel_user(client_socket,client_address)
def at_end():
    global server_socket
    server_socket.close()




if __name__ == '__main__':
    if not at_start():
        print("ho no")
    accept_client()
    at_end()