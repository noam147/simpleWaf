import requests
import sys
sys.path.append('../code')

import DB_Wrapper
from vars_for_global_use import *
WAF_IP_ADDRESS = "127.0.0.1"
PORT = 5000
url = f"http://{WAF_IP_ADDRESS}:{PORT}"

### TODO put in the linux website that in its prefrences table linux is wrote and same as the windows test

def t1est_1_windows()->bool:

    """need to reset the attacker table before using test"""
    DB_Wrapper.delete_attacker("127.0.0.1")
    existing_web_host_name = "mysite.com"
    headers = {
        "Host": existing_web_host_name
    }
    data = {"user":"admin| ipconfig"}
    response = requests.get(url,headers=headers,data=data)
    print(response)
    print(ATTACK_FOUND_CODE)

    DB_Wrapper.delete_attacker("127.0.0.1")
def t1est_2_linux()->bool:

    """need to reset the attacker table before using test"""
    DB_Wrapper.delete_attacker("127.0.0.1")
    existing_web_host_name = "mysite.com"
    headers = {
        "Host": existing_web_host_name
    }
    data = {"user":"admin| sudo rm"}
    response = requests.get(url,headers=headers,data=data)
    print(response)
    print(ATTACK_FOUND_CODE)

    DB_Wrapper.delete_attacker("127.0.0.1")
def activate_all_tests():
    #t1_est_real_web()
    t1est_1_windows()
    t1est_2_linux()
    print("test completed successfully!")
if __name__ == '__main__':
    activate_all_tests()
