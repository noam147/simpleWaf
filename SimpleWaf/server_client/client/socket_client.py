import socket
IP_ADD = '127.0.0.1'
SERVER_PORT = 47777
client_socket:socket.socket = None

def receive_data():
    global client_socket
    data = client_socket.recv(1024)
    if not data:
        print("No Data")
        return None
    #print(data)
    return data.decode('utf-8')
def send_data(message):
    global client_socket
    message += "\n"
    client_socket.sendall(message.encode('utf-8'))

def at_start() -> bool:
    """func will content the client into the server, return true if the connection established"""
    global client_socket
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((IP_ADD, SERVER_PORT))
    except Exception as e:
        return False
    return True

def at_end():
    global client_socket
    client_socket.close()