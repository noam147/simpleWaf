import requests
import sys
sys.path.append('../code')

import DB_Wrapper
from vars_for_global_use import *
WAF_IP_ADDRESS = "127.0.0.1"
PORT = 5000
url = f"http://{WAF_IP_ADDRESS}:{PORT}"

def t1_est_real_web():
    """this for testing in real world - when try this - put in routing.py line 79(for now):
     new_url = f"https://{website_ip}:/{path}" """
    host_name = "dns.google"
    headers = {
        "Host": host_name
    }
    response = requests.get(url, headers=headers)
    print(response)
def t1est_1()->bool:
    #does not work at this moment ->
    #need to put https in url, and some headres are prablomatic
    existing_web_host_name = "mysite.com"
    headers = {
        "Host": existing_web_host_name
    }
    response = requests.get(url,headers=headers)
    print(response)
    assert response.status_code == WEBSITE_NOT_RESPONDING_CODE
def t1est_2()->bool:
    not_existing_web_host_name = "my_not_existing_site.com"
    headers = {
        "Host": not_existing_web_host_name
    }

    response = requests.get(url,headers=headers)
    print(response)
    assert response.status_code == WEBSITE_NOT_EXIST_CODE
def t1est_3()->bool:
    #does not work at this moment ->
    #need to put https in url, and some headres are prablomatic
    existing_web_host_name = "mysite.com"
    headers = {
        "Host": existing_web_host_name
    }
    #malicus data:
    data = {
        "user":" 'or 1=1'"
    }
    response = requests.post(url,headers=headers,json=data)
    print(response)
    assert response.status_code == ATTACK_FOUND_CODE
def t1est_4()->bool:
    #does not work at this moment ->
    #need to put https in url, and some headres are prablomatic
    existing_web_host_name = "mysite.com?user='or 1=1'"
    headers = {
        "Host": existing_web_host_name
    }

    response = requests.get(url,headers=headers)
    print(response)
    assert response.status_code == ATTACK_FOUND_CODE
def activate_all_tests():
    #t1_est_real_web()
    t1est_1()
    t1est_2()
    t1est_3()
    t1est_4()
    print("test completed successfully!")
if __name__ == '__main__':
    activate_all_tests()
