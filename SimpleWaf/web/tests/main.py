import socket
host_add = "challenges-finals.cyber.org.il"
port = 1337
def receive_data(sock):
    data = sock.recv(1024)
    if not data:
        return None
    return data.decode('utf-8')


def send_data(sock, message):
    sock.sendall(message.encode('utf-8'))
def at_start_of_con(sock):
    receive_data(sock)
    send_data(sock,"2\n")
    receive_data(sock)
    send_data(sock,"Ca$in0M@st3r\n")
    data = receive_data(sock)
    send_data(sock, "406979561\n")
    data = receive_data(sock)
    return False,""

def win_money():
    send_data(sock, "3\n")
    data = receive_data(sock)
    send_data(sock, "1\n")
    data = receive_data(sock)

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host_add, port))
        print(f"Connected to {host}:{port}")
        try:
            at_start_of_con(s)
            for i in range(2000):
                win_money()
        except Exception as e:
            print(e)
if __name__ == '__main__':
    main()