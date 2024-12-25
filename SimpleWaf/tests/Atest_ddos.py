import unittest
import requests
import urllib.parse
import sys
import threading
sys.path.append('../code')
import DB_Wrapper

def send_msg():
    WAF_IP_ADDRESS = "127.0.0.1"
    PORT = 5000
    url = f"http://{WAF_IP_ADDRESS}:{PORT}"
    existing_web_host_name = "mysite.com"
    headers = {
        "Host": existing_web_host_name
    }
    response = requests.get(url, headers=headers)
    print(response)

def taest_ddos():
    DB_Wrapper.delete_attacker("127.0.0.1")
    while True:
        msg_to_server = threading.Thread(target=send_msg, daemon=True)
        msg_to_server.start()
        #self.assertFalse(result)- program completly stops after that- shouldnot happend


if __name__ == '__main__':
    taest_ddos()
