import requests
IP_ADD = '127.0.0.1'
SERVER_PORT = 47777
URL = f"http://{IP_ADD}:{SERVER_PORT}"

def at_start():
    response = requests.get(URL)
    return response.status_code == 200