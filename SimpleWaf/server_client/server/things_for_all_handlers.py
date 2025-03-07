import socket
def receive_data(s:socket.socket):
    data = s.recv(1024)
    if not data:
        print("No Data")
        return None
    return data.decode('utf-8')
def send_data(s:socket.socket,message):
    message += "\n"#for the sending
    s.sendall(message.encode('utf-8'))
